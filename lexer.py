__author__ = 'gleb23'

ss = '''
int odd(int i)
{
  return 2 * i + 1;
}

int square(int i)
{
  return i * i;
}

typedef boost::counting_iterator <int> counter;
typedef boost::transform_iterator <int (*)(int), counter> transformer;

transformer odds(int n)
{
  return transformer(counter(n), odd);
}

// comment
transformer squares(int n)
{
  return transformer(counter(n), square);
}

int main()
{
  using namespace std;

  cout << "Enter vector length: ";
  int n; cin >> n;

  cout << inner_product( odds(0), odds(n), squares(0), 0 ) << endl;
}
'''
# ss = ''' /*a*/


# '''

# for parsing break string into tokens

#delimiters: ' ', '\n', '{', '}', ')', '(', '[', ']', '<', '>', '=', '!', '+', '-', '/', '\"', '\'', '%', '*'

class NextTokenNotAvailable(object):
    pass


class Lexer(object):
    #delimeters that are not returned as tokens
    ignorable_delimiters = [' ', '\n']
    #delimeters that are returned as tokens and consist of one sign only
    single_sign_delimiters = ['{', '}', ')', '(', '[', ']', '\"', '\'', ',', ';']
    #delimeters that are returned as tokens and consist of either one or two signs
    #mapped values are the ones that can follow key values
    double_sign_delimiters = {'<': ['='], '>' : ['='], '=' : ['='], '!' : ['='],
                              '+' : ['+', '='], '-' : ['-', '='], '/' : ['/', '*', '='],
                              '%' : ['='], '*' : ['=']}
    current_pos = 0
    current_token_start = 0

    #
    ignoring_list = {'"': '"', '/*': '*/', '//' : '\n'}

    #
    ignoring_sequence = None
    double_sign = None

    def __init__(self, source):
        self.source = source.strip()

    def next_token(self):
        if not self.next_available():
            raise NextTokenNotAvailable()
        to_return = ""
        while self.current_pos < len(self.source) and (to_return == "" or self.ignoring_sequence != None):
            current_sym = self.source[self.current_pos]
            if self.ignoring_sequence == None and self.double_sign == None:
                if current_sym in self.ignorable_delimiters:
                    if self.current_pos > self.current_token_start:
                        to_return = self.source[self.current_token_start:self.current_pos]
                    self.current_pos += 1
                    self.current_token_start = self.current_pos
                elif current_sym in self.single_sign_delimiters:
                    if self.current_pos > self.current_token_start:
                        to_return = self.source[self.current_token_start:self.current_pos]
                        self.current_token_start = self.current_pos
                    else:
                        to_return = self.source[self.current_pos]
                        self.current_pos += 1
                        self.current_token_start = self.current_pos
                elif self.double_sign_delimiters.has_key(current_sym):
                    self.double_sign = current_sym
                    if self.current_pos > self.current_token_start:
                        to_return = self.source[self.current_token_start:self.current_pos]
                        self.current_token_start = self.current_pos
                    self.current_pos += 1
                else:
                    self.current_pos += 1
            elif self.ignoring_sequence != None:
                to_find = self.ignoring_list[self.ignoring_sequence]
                ind = self.source[self.current_pos:].find(to_find)
                if ind == -1:
                    to_return += self.source[self.current_pos:]
                    self.current_token_start = len(self.source)
                    self.current_pos = self.current_token_start
                else:
                    ind += self.current_pos
                    to_return += self.source[self.current_pos:ind+len(to_find)]
                    self.current_token_start = ind+len(to_find)
                    self.current_pos = self.current_token_start
                self.ignoring_sequence = None
            elif self.double_sign != None:
                #delimiter consists of two symbols
                if current_sym in self.double_sign_delimiters[self.double_sign]:
                    to_return = self.double_sign + current_sym
                    self.current_token_start = self.current_pos + 1
                #delimiter consists of one symbol
                else:
                    to_return = self.double_sign
                    self.current_token_start = self.current_pos
                self.current_pos += 1
                self.double_sign = None
            if self.ignoring_list.has_key(to_return):
                self.ignoring_sequence = to_return

        return to_return

    def next_available(self):
        return self.current_pos < len(self.source)

lexer = Lexer(ss)
while lexer.next_available():
    print lexer.next_token()




