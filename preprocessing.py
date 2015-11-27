import re

sym_table={}
temp_datatype_table={}

def create_sym_table(temp_head,func_sign):
	temp_head=temp_head.strip(">").split("<")[1];
	genTypes=list(map(lambda x: x.strip().split(" ")[1],temp_head.split(",")))
	for dtype in genTypes:
		temp_datatype_table[dtype]=[];
	func_sign=func_sign.strip(")").split("(")[1]
	para_list=list(map(lambda x : x.strip(),func_sign.split(",")))
	for para in para_list:
		(dtype,varname)=para.split(" ")
		if dtype in temp_datatype_table:
			sym_table[varname]=dtype
			temp_datatype_table[dtype].append(varname)

def preprocessing(filename):

        #Open the input file
        f=open(filename,"r")

        #Read the entire file as a string
        all=f.read()

        #Form a list of lines of the input file
        all=all.split("\n")

        #Remove whitespace characters from the beginning of the line and end of the line,if any
        for line_no in range(0,len(all)):
                all[line_no] = re.sub(r'^\s*',"",all[line_no])
                all[line_no] = re.sub(r'\s*$',"",all[line_no])

        #Removes all '' in the list, if present
        all = list(filter(('').__ne__, all))

        #Create the symbol table as well as template_datatype_table
        create_sym_table(all[0], all[1])

        #Get only the function body
        body=all[2:]

        #Remove lines which has only flower braces
        body[:] = [line for line in body if not(re.match(r'^[{}]$',line))]

        #Remove the line which contains only 'do' in case of do-while loop
        body[:] = [line for line in body if not(re.match(r'^do$',line))]

        #Remove the line which contains only 'else' in case of if-else loop
        body[:] = [line for line in body if not(re.match(r'^else$',line))]

        #Extracting condition expression in while or do-while loop ( IMPLEMENT NON GREEDY )
        while_pattern=r'while\((.*)\)'
        #Extracting condition expression in if loop
        if_pattern=r'if\((.*)\)'
        #Extracting condition expression in else loop
        else_pattern=r'else\((.*)\)'
        #Extracting strings and removing them
        quotes_pattern=r'\"(.*?)\"'
        #Extracting condition expression in for loop
        for_pattern=r'for\((.*)\)'

        def expression(m) :
                return m.group(1)

        def removal(m) :
                return "\"\""

        for line_no in range(0,len(body)):
                body[line_no] = re.sub(while_pattern,expression,body[line_no])
                body[line_no] = re.sub(if_pattern,expression,body[line_no])
                body[line_no] = re.sub(else_pattern,expression,body[line_no])
                body[line_no] = re.sub(quotes_pattern,removal,body[line_no])
                body[line_no] = re.sub(for_pattern,expression,body[line_no])
                #Ensures all expressions end with a semi-colon
                if(not body[line_no].endswith(";")) :
                        body[line_no]+=";"
        
        f.close()
        return body



