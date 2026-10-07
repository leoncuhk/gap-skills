"""Real shipped entry point: readable evidence, stale sources, same-use closure."""
import hashlib
import json
import shutil
import unittest
from html.parser import HTMLParser
import test_checkpoint as fixtures


class Anchors(HTMLParser):
    def __init__(self):
        super().__init__(); self.links=[]; self.ids=set()
    def handle_starttag(self, tag, attrs):
        attrs=dict(attrs)
        if tag=='a' and attrs.get('href','').startswith('#source-'): self.links.append(attrs['href'][1:])
        if 'id' in attrs: self.ids.add(attrs['id'])


class BriefCLITests(unittest.TestCase):
    setUp=fixtures.CheckpointTests.setUp
    write=fixtures.CheckpointTests.write
    cli=fixtures.CheckpointTests.cli

    def ref(self, name, start=1, end=1):
        path=self.root/name
        return {'path':name,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
                'target':str(path.resolve().relative_to(self.root.resolve())), 'start':start,'end':end}

    def brief(self):
        self.write('before.txt','错误：21张\n历史推断未验证')
        self.write('after.txt','更正：17张\n未发货')
        self.write('policy.txt','相同请求取最高修订；不同请求不合并。\n运送须由项目负责人决定。')
        data={'version':1,'summary':'更正总数，保留运送决定。','changes':[{'criterion':'output',
              'title':'修正补发数量','impact':'少4张，不能等同已运送','claim_type':'source_fact',
              'before':self.ref('before.txt'),'after':self.ref('after.txt'),'basis':[self.ref('policy.txt',1,2)]}],
              'decisions':[],'limits':['浏览器与真人理解未测。']}
        self.write('brief.json',data);return data

    def render(self, name, kind='html', helper=fixtures.HELPER, details=False):
        observation=self.cli('view','--brief','brief.json','--format',kind,'--output',str(self.root/name),*(['--details'] if details else []),helper=helper)
        return observation,(self.root/name).read_text()

    def payload(self, observation):
        self.write('feedback.json',{'version':1,'observation_sha256':observation['observation_sha256'],
                   'feedback':[{'criterion':'output','decision':'question','note':'运送负责人尚未选择'}]})

    def test_installed_text_html_contain_real_excerpts_diff_and_native_links(self):
        self.brief(); before=self.state.read_bytes()
        installed=self.root/'installed';shutil.copytree(fixtures.ROOT/'skills/gap',installed)
        obs,html=self.render('review.html',helper=installed/'scripts/checkpoint.py')
        compact,summary=self.render('summary.txt','text',helper=installed/'scripts/checkpoint.py')
        other,text=self.render('review.txt','text',helper=installed/'scripts/checkpoint.py',details=True)
        self.assertEqual(compact['observation_sha256'],obs['observation_sha256'])
        self.assertIn('--details',summary);self.assertIn('policy.txt:1-2',summary)
        self.assertIn(obs['observation_sha256'],summary);self.assertIn('Brief: brief.json',summary)
        self.assertNotIn('错误：21张',summary);self.assertIn('少4张',summary)
        self.assertEqual(obs,other | {'output':obs['output']})
        for fact in ['错误：21张','更正：17张','少4张','相同请求取最高修订']:
            self.assertIn(fact,html);self.assertIn(fact,text)
        self.assertIn('-错误：21张',html);self.assertIn('+更正：17张',text)
        anchors=Anchors();anchors.feed(html)
        self.assertTrue(anchors.links);self.assertTrue(set(anchors.links)<=anchors.ids)
        self.payload(obs)
        feedback=self.cli('feedback','--brief','brief.json','--file','feedback.json')
        self.assertFalse(feedback['applied']);self.assertFalse(feedback['authorization'])
        self.assertEqual(before,self.state.read_bytes())

    def test_uncited_line_and_brief_edits_invalidate_returned_feedback(self):
        self.brief();obs,_=self.render('review.html');self.payload(obs)
        self.write('before.txt','错误：21张\n来源新修订')
        self.cli('feedback','--brief','brief.json','--file','feedback.json',expected=2)
        fresh,html=self.render('stale.html');self.assertIn('Brief is stale; recheck sources:',html)
        self.payload(fresh)
        self.cli('feedback','--brief','brief.json','--file','feedback.json',expected=2)
        data=self.brief();obs,_=self.render('fresh.html');self.payload(obs)
        data['summary']='另一种解读';self.write('brief.json',data)
        self.cli('feedback','--brief','brief.json','--file','feedback.json',expected=2)

    def test_human_options_required_and_cannot_be_empty(self):
        self.contract['criteria'].append({'id':'ship','kind':'human','claim':'负责人选运送方式'})
        self.write('contract.json',self.contract)
        self.cli('revise','--contract',str(self.root/'contract.json'),'--authority','test user','--reason','decision pending')
        data=self.brief()
        self.cli('view','--brief','brief.json',expected=2)
        data['decisions']=[{'criterion':'ship','question':'何时运送？','owner':'项目负责人','deferral':'保留本地，交付时间未定',
            'options':[{'id':'now','label':'现在运送','consequence':'提前收到','tradeoff':'成本高'},
                       {'id':'later','label':'稍后运送','consequence':'较晚收到','tradeoff':'成本低'}]}]
        self.write('brief.json',data);_,html=self.render('choices.html')
        self.assertIn('项目负责人',html);self.assertIn('较晚收到',html)
        data['decisions'][0]['options'][1]['consequence']=''
        self.write('brief.json',data);self.cli('view','--brief','brief.json',expected=2)

    def test_symlink_target_change_and_html_injection(self):
        data=self.brief();self.write('same.txt',(self.root/'before.txt').read_text())
        (self.root/'alias.txt').symlink_to('before.txt')
        data['changes'][0]['before']=self.ref('alias.txt')
        data['summary']='</script><img src=x onerror=alert(1)>'
        self.write('brief.json',data);obs,html=self.render('review.html');self.payload(obs)
        self.assertNotIn('<img src=x',html)
        (self.root/'alias.txt').unlink();(self.root/'alias.txt').symlink_to('same.txt')
        self.cli('feedback','--brief','brief.json','--file','feedback.json',expected=2)

    def test_version_and_span_are_strict_and_cannot_inject_quote(self):
        for field,value in [('version',True),('version',1.0)]:
            data=self.brief();data[field]=value;self.write('brief.json',data)
            self.cli('view','--brief','brief.json',expected=2)
        for field,value in [('start',True),('end',200),('text','forged quote'),('path','../source.txt')]:
            data=self.brief();data['changes'][0]['before'][field]=value;self.write('brief.json',data)
            self.cli('view','--brief','brief.json',expected=2)

    def test_selected_brief_identity_is_bound_even_when_both_are_inputs(self):
        data=self.brief();data['summary']='另一份需要单独核查的解释'
        self.write('other-brief.json',data)
        self.contract['inputs'] += ['brief.json','other-brief.json']
        self.write('contract.json',self.contract)
        self.cli('revise','--contract',str(self.root/'contract.json'),'--authority','test user','--reason','both sources known')
        observation,_=self.render('first.html');self.payload(observation)
        result=self.cli('feedback','--brief','other-brief.json','--file','feedback.json',expected=2)
        self.assertIn('stale feedback',result['error'])

    def test_evidence_links_expand_ancestors_and_focus_target_without_browser(self):
        import subprocess
        if not shutil.which('node'):
            self.skipTest('Node unavailable; no browser claim')
        self.brief();fixtures.CheckpointTests.record(self)
        self.render('links.html')
        script = r"""
const fs=require('fs'),vm=require('vm'),assert=require('assert');
const page=fs.readFileSync(process.argv[2],'utf8');
const binding=page.match(/<script type="application\/json" id="binding">([\s\S]*?)<\/script>/)[1];
const code=page.split('<script>')[1].split('</script>')[0];
const elements={};
function el(id){return elements[id]??={value:'',textContent:'',events:{},tagName:'DIV',parentElement:null,open:false,addEventListener(k,f){this.events[k]=f},setAttribute(k,v){this[k]=v},focus(){this.focused=true},scrollIntoView(){this.scrolled=true}};}
el('binding').textContent=binding;
const ids=['source-0','receipt-0'];
const anchors=ids.map(id=>({events:{},getAttribute:()=> '#'+id,addEventListener(k,f){this.events[k]=f}}));
for(const id of ids){assert(page.includes('href="#'+id+'"'));el(id).parentElement=el('parent-'+id);el('parent-'+id).tagName='DETAILS';}
el('source-0').tagName='DETAILS';
const document={getElementById:el,querySelectorAll:q=>q==='a[data-evidence-target]'?anchors:[],createElement:()=>({click(){}})};
vm.runInNewContext(code,{document,Blob:class{},URL:{},setTimeout(){}});
anchors.forEach((a,i)=>{a.events.click();assert(el('parent-'+ids[i]).open);assert(el(ids[i]).focused);assert(el(ids[i]).scrolled);assert.equal(el(ids[i]).tabindex,'-1');});
assert(el('source-0').open);
console.log('PASS: simulated source/receipt links expand ancestors, focus and scroll; not browser QA');
"""
        path=self.root/'check-links.cjs';path.write_text(script)
        result=subprocess.run(['node',str(path),str(self.root/'links.html')],text=True,capture_output=True)
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)

    def test_use_result_cli_task_revision_and_stale_result(self):
        self.write('lesson.md','Candidate: verify replacement semantics, not row order.')
        data=self.cli('use','--file','lesson.md','--status','candidate','--decision','trial','--reason','matching task')
        use=data['experience_uses'][0];self.assertEqual(use['task_id'],data['task_id'])
        self.assertEqual(use['current_result_status'],'unverified')
        self.write('actual-check.txt','Synthetic local positive control: expected 17, got 17.')
        ref=self.ref('actual-check.txt');ref.pop('start');ref.pop('end')
        result={'use_id':use['id'],'task_id':data['task_id'],'experience_id':use['experience_id'],
                'outcome':'pass','observed':'test fixture result','cost':'unknown','user_intervention':'unknown','checks':[ref]}
        self.write('result.json',result)
        closed=self.cli('use-result','--use-id',use['id'],'--receipt','result.json','--outcome','pass')
        self.assertEqual(closed['experience_uses'][0]['current_result_status'],'recorded')
        self.write('source.txt','Changed contract input outside experience files')
        self.assertEqual(self.cli('check',expected=1)['experience_uses'][0]['current_result_status'],'stale')
        self.write('source.txt','original')
        self.write('actual-check.txt','Changed result')
        self.assertEqual(self.cli('check',expected=1)['experience_uses'][0]['current_result_status'],'stale')
        self.contract['purpose']='Revised purpose';self.write('contract.json',self.contract)
        self.cli('revise','--contract',str(self.root/'contract.json'),'--authority','test user','--reason','changed purpose')
        self.cli('use-result','--use-id',use['id'],'--receipt','result.json','--outcome','pass',expected=2)

if __name__=='__main__':unittest.main()
