#[c]All pattern variables must start with 'p_'.

p_inline_ws	= ' [^\n\S]* '
p_something	= ' .+ '
p_maybe_something	= ' .* '
p_do_not_backtrack	= ' (*SKIP) '
p_function_keyword	= ' ^  {{ inline ws }}  \m  def    \M '
p_class_keyword	= ' ^  {{ inline ws }}  \m  class  \M '
p_three_dots	= ' \.\.\. '

if __name__ == '__main__':
	print('Nope, the run.py does the job')
