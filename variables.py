#[of]:Inline Whitespace
p_inline_ws = r'[^\S\n]'
#[cf]
#[of]:Two or more newlines
p_newlines = r'(?:\n\s*\n)'
#[cf]

#[of]:Attributes
#[c]partially taken from the TiddlyWiki Codebase
#[c]

#[of]:String literal
p_string_literal = r'''(?:

	""" [\s\S]*? """
	|
	" [^"]* "
	|
	' [^']* '

)'''
#[cf]
#[of]:Unquoted attribute value
p_unquoted_attribute_value = r'''(?:

	[^\s<>"'=/]+

)'''
#[cf]
#[of]:Filtered attribute value
p_filtered_attribute_value = r'''(?:

	\{\{\{
	[\s\S]+?
	\}\}\}

)'''
#[cf]
#[of]:Indirect attribute value
p_indirect_attribute_value = r'''(?:

	\{\{
	[^\}]+
	\}\}

)'''
#[cf]
#[of]:Macro call
p_macro_call = r'''(?:

	<<
	[^>\s]+
	\s*
	(?:
		[^>]
		|
		(?:
			>
			(?!>)
		)
	)*?
	>>

)'''
#[cf]
#[of]:Double square brackets
p_double_square_brackets = r'''(?:

	\[\[
	[^\]]*
	\]\]

)'''
#[cf]

#[of]:Attribute name
p_attribute_name = r'''(?:

	[$a-zA-Z_]
	(?:
		-? [a-zA-Z0-9_]+
	)* (*PRUNE)

)'''
#[cf]
#[of]:Attribute value
p_attribute_value = '''(?:

	{{String literal}}
	|
	{{Unquoted attribute value}}
	|
	{{Filtered attribute value}}
	|
	{{Indirect attribute value}}
	|
	{{Macro call}}

)'''
#[cf]
#[of]:Attribute
p_attribute = r'''(?:

	\s+
	{{Attribute name}}
	\s* = \s*
	{{Attribute value}}

)'''
#[cf]
#[of]:Attributes
p_attributes = r'''(?:

	{{attribute}}*

)'''
#[cf]
#[cf]
#[of]:Tag Names
#[of]:Any
p_any_tag_name = r'''(?:

	[$]?
	[a-zA-Z]
	(?:
		-?[a-zA-Z0-9_]+
	)* (*PRUNE)
	(?=[\s/>])

)'''
#[cf]
#[of]:Block
p_block_tag_name = r'''(?:

	(?:
		div|section|article|aside|details|nav|
		table|ul|ol|dl|
		header|hgroup|h[1-6]|footer|
		blockquote|pre|figure|
		form|fieldset
	)
	(?=[\s/>])

)'''
#[cf]
#[of]:Widget
p_widget_tag_name = r'''(?:

	[$]
	(?:
		action-
		(?:
			createtiddler|deletefield|deletetiddler|
			listops|navigate|sendmessage|setfield
		)
		|
		browse|button|checkbox|codeblock|count|
		diff-text|draggable|droppable|dropzone|
		edit-bitmap|edit-text|edit|encrypt|entity|
		fieldmangler|fields|image|importvariables|
		keyboard|linkcatcher|link|list|macrocall|
		navigator|password|radio|range|reveal|
		scrollable|select|setvariable|set|
		text|tiddler|transclude|vars|view|wikify
	)
	(?=[\s/>])

)'''
#[cf]
#[of]:Inline
p_inline_tag_name = r'''(?:

	(?:
		abbr|audio|bdi|bdo|button|cite|code|
		del|dfn|em|input|kbd|mark|meter|output|
		progress|ruby|samp|small|span|
		strong|sub|sup|time|var|wbr|
		b|i|q|s|u
	)
	(?=[\s/>])

)'''
#[cf]
#[of]:Widget or inline
p_widget_or_inline_tag_name = '''(?:

	{{Widget tag name}}
	|
	{{Inline tag name}}

)'''
#[cf]
#[cf]
#[of]Open Tags:Open Tags
p_tag_opener = r'(?<!<) <'
p_tag_closer = r'> (?!>)'

#[of]Any:Any
p_any_open_tag = r'''(?:

	{{Tag opener}}
	{{Any tag name}}
	{{Attributes}}
	\s* (*PRUNE)
	{{Tag closer}}

)'''
#[cf]
#[of]:Inline
p_inline_open_tag = r'''(?:

	{{Tag opener}}
	{{inline_tag_name}}
	{{attributes}}
	\s*
	(*PRUNE)
	{{Tag closer}}

)'''
#[cf]
#[of]:Widget
p_widget_open_tag = r'''(?:

	{{Tag opener}}
	{{widget_tag_name}}
	{{attributes}}
	\s*
	(*PRUNE)
	{{Tag closer}}

)'''
#[cf]
#[of]:Widget or inline
p_widget_or_inline_open_tag = r'''(?:

	{{Tag opener}}
	{{Widget or inline tag name}}
	{{Attributes}}
	\s*
	(*PRUNE)
	{{Tag closer}}

)'''
#[cf]
#[cf]

if __name__ == '__main__':
	print('Nope, the run.py does the job')
