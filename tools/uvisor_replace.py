import fileinput
import re
import argparse

# parse input arguments
parser = argparse.ArgumentParser(description="""Search and replace Freescale pre-processor
                                             macros for memory access with uvisor ones""",
                                 usage='%(prog)s filename(s)')
parser.add_argument('filenames', nargs='+', help='input file(s) to process', metavar='FILE')
parser.parse_args()

# regex array
regex_dict = []

# regular memory write operation (32/16/8bits)
#   2 arguments (x, v)
#   note: using lambda to access lower() method for group 2
regex_dict.append({
    'src': r'(#define\s+BW_[A-Za-z_0-9]+\(x, v\)\s+\()(HW_[A-Za-z_0-9]+)_WR\(x, (.*v.*)\)\)',
    'dst': lambda p: p.group(1) + 'UNION_WRITE_REG_FS(' + p.group(2) + '_ADDR(x), ' + p.group(2).lower() + ', ' + p.group(3) + '))'
})

# regular memory write operation (32/16/8bits)
#   3 arguments (x, n, v)
#   note: using lambda to access lower() method for group 2
regex_dict.append({
    'src': r'(#define\s+BW_[A-Za-z_0-9]+\(x, n, v\)\s+\()(HW_[A-Za-z_0-9]+)_WR\(x, n, (.*v.*)\)\)',
    'dst': lambda p: p.group(1) + 'UNION_WRITE_REG_FS(' + p.group(2) + '_ADDR(x, n), ' + p.group(2).lower() + ', ' + p.group(3) + '))'
})

# bitband write operation (32bits)
#   2 arguments (x, v)
regex_dict.append({
    'src': r'(#define\s+BW_[A-Za-z_0-9]+\(x, v\)\s+\()BITBAND_ACCESS32\((.+)\) = \(v\)\)',
    'dst': r'\g<1>ADDRESS_WRITE32(BITBAND_ADDRESS32(\g<2>), v))'
})

# bitband write operation (32bits)
#   3 arguments (x, n, v)
regex_dict.append({
    'src': r'(#define\s+BW_[A-Za-z_0-9]+\(x, n, v\)\s+\()BITBAND_ACCESS32\((.+)\) = \(v\)\)',
    'dst': r'\g<1>ADDRESS_WRITE32(BITBAND_ADDRESS32(\g<2>), v))'
})

# bitband write operation (16bits)
#   2 arguments (x, v)
regex_dict.append({
    'src': r'(#define\s+BW_[A-Za-z_0-9]+\(x, v\)\s+\()BITBAND_ACCESS16\((.+)\) = \(v\)\)',
    'dst': r'\g<1>ADDRESS_WRITE16(BITBAND_ADDRESS16(\g<2>), v))'
})

# bitband write operation (16bits)
#   3 arguments (x, n, v)
regex_dict.append({
    'src': r'(#define\s+BW_[A-Za-z_0-9]+\(x, n, v\)\s+\()BITBAND_ACCESS16\((.+)\) = \(v\)\)',
    'dst': r'\g<1>ADDRESS_WRITE16(BITBAND_ADDRESS16(\g<2>), v))'
})

# bitband write operation (8bits)
#   2 arguments (x, v)
regex_dict.append({
    'src': r'(#define\s+BW_[A-Za-z_0-9]+\(x, v\)\s+\()BITBAND_ACCESS8\((.+)\) = \(v\)\)',
    'dst': r'\g<1>ADDRESS_WRITE8(BITBAND_ADDRESS8(\g<2>), v))'
})

# bitband write operation (8bits)
#   3 arguments (x, n, v)
regex_dict.append({
    'src': r'(#define\s+BW_[A-Za-z_0-9]+\(x, n, v\)\s+\()BITBAND_ACCESS8\((.+)\) = \(v\)\)',
    'dst': r'\g<1>ADDRESS_WRITE8(BITBAND_ADDRESS8(\g<2>), v))'
})

# regular memory read operation (32/16/8bits)
#   1 argument (x)
#   access to specific bitfields
#   note: using lambda to access lower() method for group 2
regex_dict.append({
    'src': r'(#define\s+BR_[A-Za-z_0-9]+\(x\)\s+\()(HW_[A-Za-z_0-9]+)\(x\)\.B\.(.+)\)',
    'dst': lambda p: p.group(1) + 'UNION_READ_BIT_FS(' + p.group(2) + '_ADDR(x), ' + p.group(2).lower() + ', B.' + p.group(3) + '))'
})

# regular memory read operation (32/16/8bits)
#   1 argument (x)
#   access to whole register content
#   note: using lambda to access lower() method for group 2
regex_dict.append({
    'src': r'(#define\s+BR_[A-Za-z_0-9]+\(x\)\s+\()(HW_[A-Za-z_0-9]+)\(x\)\.U\)',
    'dst': lambda p: p.group(1) + 'UNION_READ_REG_FS(' + p.group(2) + '_ADDR(x), ' + p.group(2).lower() + '))'
})

# regular memory read operation (32/16/8bits)
#   2 arguments (x, n)
#   access to specific bitfields
#   note: using lambda to access lower() method for group 2
regex_dict.append({
    'src': r'(#define\s+BR_[A-Za-z_0-9]+\(x, n\)\s+\()(HW_[A-Za-z_0-9]+)\(x, n\)\.B\.(.+)\)',
    'dst': lambda p: p.group(1) + 'UNION_READ_BIT_FS(' + p.group(2) + '_ADDR(x, n), ' + p.group(2).lower() + ', B.' + p.group(3) + '))'
})

# regular memory read operation (32/16/8bits)
#   2 arguments (x, n)
#   access to whole register content
#   note: using lambda to access lower() method for group 2
regex_dict.append({
    'src': r'(#define\s+BR_[A-Za-z_0-9]+\(x, n\)\s+\()(HW_[A-Za-z_0-9]+)\(x, n\)\.U\)',
    'dst': lambda p: p.group(1) + 'UNION_READ_REG_FS(' + p.group(2) + '_ADDR(x, n), ' + p.group(2).lower() + '))'
})

# bitband read operation (32bits)
#   1 argument (x)
regex_dict.append({
    'src': r'(#define\s+BR_[A-Za-z_0-9]+\(x\)\s+\()BITBAND_ACCESS32\((.+)\)\)',
    'dst': r'\g<1>ADDRESS_READ32(BITBAND_ADDRESS32(\g<2>)))'
})

# bitband read operation (32bits)
#   2 arguments (x, n)
regex_dict.append({
    'src': r'(#define\s+BR_[A-Za-z_0-9]+\(x, n\)\s+\()BITBAND_ACCESS32\((.+)\)\)',
    'dst': r'\g<1>ADDRESS_READ32(BITBAND_ADDRESS32(\g<2>)))'
})

# bitband read operation (16bits)
#   1 argument (x)
regex_dict.append({
    'src': r'(#define\s+BR_[A-Za-z_0-9]+\(x\)\s+\()BITBAND_ACCESS16\((.+)\)\)',
    'dst': r'\g<1>ADDRESS_READ16(BITBAND_ADDRESS16(\g<2>)))'
})

# bitband read operation (16bits)
#   2 arguments (x, n)
regex_dict.append({
    'src': r'(#define\s+BR_[A-Za-z_0-9]+\(x, n\)\s+\()BITBAND_ACCESS16\((.+)\)\)',
    'dst': r'\g<1>ADDRESS_READ16(BITBAND_ADDRESS16(\g<2>)))'
})

# bitband read operation (8bits)
#   1 argument (x)
regex_dict.append({
    'src': r'(#define\s+BR_[A-Za-z_0-9]+\(x\)\s+\()BITBAND_ACCESS8\((.+)\)\)',
    'dst': r'\g<1>ADDRESS_READ8(BITBAND_ADDRESS8(\g<2>)))'
})

# bitband read operation (8bits)
#   2 arguments (x, n)
regex_dict.append({
    'src': r'(#define\s+BR_[A-Za-z_0-9]+\(x, n\)\s+\()BITBAND_ACCESS8\((.+)\)\)',
    'dst': r'\g<1>ADDRESS_READ8(BITBAND_ADDRESS8(\g<2>)))'
})

# iterate over all lines in given input files
# no backup file is create since it is exepcted to run the script within git
lines_changed = 0
for line in fileinput.input(inplace=1):
    # iterate over all regular expressions (stop at the first one matching)
    for rgx in regex_dict:
        [line, n] = re.subn(rgx['src'], rgx['dst'], line.rstrip())
        if n > 0:
            lines_changed = lines_changed + 1
            break

    # write line to file (fileinput automatically redirects output to file)
    print(line)

# print quick report
if(lines_changed == 1):
    print('Changed ' + str(lines_changed) + ' line')
else:
    print('Changed ' + str(lines_changed) + ' lines')
