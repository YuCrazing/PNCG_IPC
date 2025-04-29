def convert_indexing(input_file, output_file, header_lines, indices_per_line):
    with open(input_file, 'r') as fin, open(output_file, 'w') as fout:
        lines = fin.readlines()
        # Copy header lines without modification
        for i in range(header_lines):
            # fout.write(lines[i])
            parts = lines[i].strip().split()
            fout.write(' '.join(parts[:1]) + '\n')
        # Process index lines
        for line in lines[header_lines:-1]:
            parts = line.strip().split()
            if len(parts) < indices_per_line:
                fout.write(line)
                continue
            # Convert indices from 1-based to 0-based
            indices = [str(int(p) - 1) for p in parts[:indices_per_line]]
            if input_file.endswith('.face'):
                fout.write(' '.join(indices) + '\n')
            else:
                fout.write(' '.join(indices + parts[indices_per_line:]) + '\n')

# # Convert .ele file (assuming 1 header line and 4 indices per line)
# convert_indexing('cube.ele', 'cube_zero.ele', header_lines=1, indices_per_line=4)

# # Convert .face file (assuming 1 header line and 3 indices per line)
# convert_indexing('cube.face', 'cube_zero.face', header_lines=1, indices_per_line=3)

# # Convert .node file (assuming 1 header line and 1 index per line)
# convert_indexing('cube.node', 'cube_zero.node', header_lines=1, indices_per_line=1)


if __name__ == "__main__":
    import sys
    args = sys.argv[1:]
    path = args[0]
    ele_file = path + '.ele'
    node_file = path + '.node'
    face_file = path + '.face'

    output_ele_file = path + '_0.ele'
    output_node_file = path + '_0.node'
    output_face_file = path + '_0.face'
    
    convert_indexing(ele_file, output_ele_file, header_lines=1, indices_per_line=5)
    convert_indexing(node_file, output_node_file, header_lines=1, indices_per_line=1)
    convert_indexing(face_file, output_face_file, header_lines=1, indices_per_line=4)
