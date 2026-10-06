import json
import subprocess
import sys
import unittest
from html.parser import HTMLParser
import test_checkpoint as fixtures


class ScriptData(HTMLParser):
    def __init__(self):
        super().__init__()
        self.binding = False
        self.data = ''
    def handle_starttag(self, tag, attrs):
        self.binding = tag == 'script' and dict(attrs).get('id') == 'binding'
    def handle_endtag(self, tag):
        if tag == 'script': self.binding = False
    def handle_data(self, data):
        if self.binding: self.data += data


class ReviewViewTests(unittest.TestCase):
    setUp = fixtures.CheckpointTests.setUp
    write = fixtures.CheckpointTests.write
    cli = fixtures.CheckpointTests.cli
    record = fixtures.CheckpointTests.record

    def view(self, format='html', name='view.html'):
        result = self.cli('view', '--format', format, '--output', str(self.root / name))
        return result, (self.root / name).read_text()

    def payload(self, observation):
        return {'version': 1, 'observation_sha256': observation,
                'feedback': [{'criterion': 'output', 'decision': 'correction', 'note': '保留原件 "x" </script> & <b>原话</b>'}]}

    def test_text_html_share_current_observation_and_do_not_modify_state(self):
        self.record()
        before = self.state.read_bytes()
        text, body = self.view('text', 'view.txt')
        html, page = self.view()
        self.assertEqual(text['observation_sha256'], html['observation_sha256'])
        self.assertEqual(before, self.state.read_bytes())
        self.assertIn('original bytes preserved', body)
        parser = ScriptData(); parser.feed(page)
        binding = json.loads(parser.data)
        self.assertEqual(binding['observation_sha256'], html['observation_sha256'])
        self.assertEqual(binding['ids'], ['output', 'tests'])
        self.cli('view', '--output', str(self.state), expected=2)

    def test_feedback_roundtrip_is_input_not_approval(self):
        view, _ = self.view()
        payload = self.payload(view['observation_sha256'])
        self.write('feedback.json', payload)
        before = self.state.read_bytes()
        result = self.cli('feedback', '--file', 'feedback.json')
        self.assertEqual(result['feedback'], payload['feedback'])
        self.assertIs(result['applied'], False)
        self.assertIs(result['authorization'], False)
        self.assertEqual(before, self.state.read_bytes())

    def test_file_change_invalidates_feedback_without_state_change(self):
        self.record()
        view, _ = self.view()
        self.write('feedback.json', self.payload(view['observation_sha256']))
        before = self.state.read_bytes()
        self.write('output.txt', 'changed after review')
        result = self.cli('feedback', '--file', 'feedback.json', expected=2)
        self.assertIn('stale feedback', result['error'])
        self.assertEqual(before, self.state.read_bytes())

    def test_changed_consulted_experience_invalidates_feedback(self):
        self.write('experience.md', 'Candidate: inspect capacity by workshop')
        self.cli('use', '--file', 'experience.md', '--status', 'candidate', '--decision', 'trial', '--reason', 'check actual data')
        view, page = self.view()
        self.assertIn('experience.md', page)
        self.write('feedback.json', self.payload(view['observation_sha256']))
        self.write('experience.md', 'Changed claim after feedback')
        self.cli('feedback', '--file', 'feedback.json', expected=2)
        _, text = self.view('text', 'experience-view.txt')
        self.assertIn("stale: ['experience.md']", text)

    def test_feedback_version_requires_integer_not_boolean_or_float(self):
        view, _ = self.view()
        for version in [True, 1.0, '1']:
            payload = self.payload(view['observation_sha256']); payload['version'] = version
            self.write('feedback.json', payload)
            self.cli('feedback', '--file', 'feedback.json', expected=2)

    def test_unknown_duplicate_and_unauthorized_fields_rejected(self):
        view, _ = self.view()
        for mutation in ['unknown', 'duplicate', 'approve', 'empty']:
            payload = self.payload(view['observation_sha256'])
            if mutation == 'unknown': payload['feedback'][0]['criterion'] = 'other'
            if mutation == 'duplicate': payload['feedback'] *= 2
            if mutation == 'approve': payload['approve'] = True
            if mutation == 'empty': payload['feedback'][0]['note'] = ''
            self.write('feedback.json', payload)
            self.cli('feedback', '--file', 'feedback.json', expected=2)

    def test_untrusted_source_strings_cannot_escape_html_or_json(self):
        self.contract['purpose'] = '</script><img src=x onerror=alert(1)> 测试'
        self.contract['criteria'][0]['id'] = '</script><svg/onload=alert(1)>'
        self.write('contract.json', self.contract)
        self.cli('revise', '--contract', str(self.root / 'contract.json'), '--authority', 'test input', '--reason', 'escaping regression')
        _, page = self.view()
        self.assertNotIn('<img src=x', page)
        self.assertNotIn('<svg/onload', page)
        parser = ScriptData(); parser.feed(page)
        self.assertEqual(json.loads(parser.data)['ids'][0], self.contract['criteria'][0]['id'])

    def test_export_logic_and_download_failure_without_browser(self):
        import shutil
        if not shutil.which('node'):
            self.skipTest('Node unavailable; browser-independent JS check only')
        self.view()
        test_script = r"""
const fs=require('fs'),vm=require('vm'),assert=require('assert');
const page=fs.readFileSync(process.argv[2],'utf8');
const binding=page.match(/<script type="application\/json" id="binding">([\s\S]*?)<\/script>/)[1];
const code=page.split('<script>')[1].split('</script>')[0];
const elements={};
function element(id){return elements[id]??=( {value:'',textContent:'',events:{},addEventListener(k,f){this.events[k]=f}} );}
element('binding').textContent=binding;
const document={getElementById:element,querySelectorAll:()=>[],createElement:()=>({click(){}})};
vm.runInNewContext(code,{document,Blob:class{},URL:{createObjectURL(){throw Error('blocked download')},revokeObjectURL(){}},setTimeout(){}});
element('decision-0').value='correction';element('note-0').value='原件 "x" </script> & <b>文本</b>';
element('prepare').events.click();
let exported=JSON.parse(element('output').value);
assert.equal(exported.feedback[0].note,element('note-0').value);
assert.equal(exported.observation_sha256,JSON.parse(binding).observation_sha256);
element('download').events.click();assert(element('message').textContent.includes('Copy the complete JSON'));
assert.equal(JSON.parse(element('output').value).feedback[0].note,element('note-0').value);
element('note-0').events.input();assert.equal(element('output').value,'');
element('note-0').value='';element('prepare').events.click();assert.equal(element('output').value,'');
console.log('PASS: non-browser JS modify/export/read-back, failure fallback and stale-preview clearing');
"""
        script = self.root / 'check-export.cjs'; script.write_text(test_script)
        result = subprocess.run(['node', str(script), str(self.root/'view.html')], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout+result.stderr)

    def test_shipped_folder_supports_view_without_repository_imports(self):
        import shutil
        installed = self.root / 'installed'
        shutil.copytree(fixtures.ROOT / 'skills/gap', installed)
        helper = installed / 'scripts/checkpoint.py'
        result = self.cli('view', '--format', 'text', '--output', str(self.root / 'portable.txt'), helper=helper)
        self.assertTrue(result['observation_sha256'])


if __name__ == '__main__': unittest.main()
