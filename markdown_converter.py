#!/usr/bin/python

import re, os, sys
from optparse import OptionParser


def convertText(c):
    # replace all links
    # c = re.sub(r'\[([^\]]+)\]\(([^\]]+)\)', r'[\1|\2]', c)
    c = re.sub(r'\[(.*?)\]\((.*?)\)', r'[\1|\2]', c)

    # replace bold temporarily
    c = re.sub(r'\*\*(.*?)\*\*', r'bdirkb\1bdirkb', c)
    # replace italics
    c = re.sub(r'\*(.*?)\*', r'_\1_', c)
    # replace bold
    c = re.sub(r'bdirkb(.*?)bdirkb', r'*\1*', c)

    # replace inline code
    c = re.sub(r'`(.*?)`', r'*\1*', c)

    # print c
    c = c.split('\n')

    words = []
    words.append( ['#','h1.'] )
    words.append( ['##','h2.'] )
    words.append( ['###','h3.'] )
    words.append( ['####','h4.'] )
    words.append( ['#####','h5.'] )
    words.append( ['######','h6.'] )

    newContent = []

    i = 0
    isCode = 0
    indent = 0
    isQuote = 0
    isList = 0

    for l in c:
      i += 1
      if 0 == 0:
        # print l[:30]
        k = l
        if l[0:1]=='*':
          isList = 1
        if l == '':
          isList = 0

        if l[0:1] == '>':
          if isQuote==0:
            k = '{quote}\n'+k[1:]
            isQuote = 1
          else:
            k = k[1:]


        if isList == 0:
          if isCode == 1:
            if l[0:1] == ' ' or l[0:1]=='\t':
              k = k[indent:]  
            else:
              k = '{code}\n'+k
              isCode = 0
              indent = -1
          else:
            if l[0:1]==' ' or l[0:1]=='\t':
              indent = len(k)-len(k.lstrip())
              k = '{code}\n'+k[indent:]              
              isCode = 1
        else:
           if l[0:4]=='\t\t\t*':
             k = '****' + l[4:]
           if l[0:3]=='\t\t*':
             k = '***' + l[3:]
           if l[0:2]=='\t*':
             k = '**' + l[2:]

        for w in words:
          # print l[:len(w[0])]
          if l[:len(w[0])] == w[0]:
            k = w[1]+l[len(w[0]):]


        if l[0:1] != '>' and isQuote == 1:
          k = '{quote}\n'+k
          isQuote = 0


        if l[0:3] != '| -':
          newContent.append(k)

        # print k
        i# newContent.append(k)

    return '\n'.join(newContent)



def convertFile(filename,output_dir):
    old_content = open(filename, 'r').read()
    new_content = convertText(old_content)
    if output_dir != None:
        open('%s/%s.txt' % (output_dir,filename),'w').write(new_content)
    else:
        open(filename+'.txt','w').write(new_content)
    print "converted",filename



def convertAllFiles(dirname,output_dir):
  f_counter = 0
  for f in os.listdir(dirname):

      fname = os.path.join(dirname,f)

      if fname[-3:] =='.md':
          f_counter += 1
          convertFile(fname,output_dir)

def init_options():
    usage="%prog [options] input_files.txt"
    parser = OptionParser(usage)
    parser.add_option("--output_dir",dest="output_dir",help="Output all files to a specified directory")
    return parser.parse_args()

if __name__=='__main__':

    (options,args) = init_options()

    if options.output_dir != None and not os.path.exists(options.output_dir):
        os.mkdir(options.output_dir)

    if len(args) == 0:
        convertAllFiles(".",options.output_dir)
        sys.exit()

    infile = args[0]

    if not os.path.exists(infile):
        sys.stderr("%s does not exist!" %infile)
        sys.exit(15)

    if os.path.isdir(infile):
        convertAllFiles(infile,options.output_dir)

    else:
        convertFile(infile,options.output_dir)


