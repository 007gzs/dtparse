from dateutil.parser import _timelex

from build_pycompat import tests

def main():
    with open('src/tests/pycompat_tokenizer.rs', 'w+') as handle:
        handle.write(TEST_HEADER)

        counter = 0
        for _, test_strings in tests.items():
            for s in test_strings:
                handle.write(build_test(counter, s))
                counter += 1

def build_test(i, test_string):
    python_tokens = list(_timelex(test_string))
    formatted_tokens = 'vec!["' + '", "'.join(python_tokens) + '"]'
    return f'''
#[test]
fn test_tokenize{i}() {{
    let comp = {formatted_tokens};
    tokenize_assert("{test_string}", comp);
}}\n'''


TEST_HEADER = '''
use tokenize::Tokenizer;

fn tokenize_assert(test_str: &str, comparison: Vec<&str>) {
    let tokens: Vec<String> = Tokenizer::new(test_str).collect();
    assert_eq!(tokens, comparison, "Tokenizing mismatch for `{}`", test_str);
}\n'''

if __name__ == '__main__':
    main()