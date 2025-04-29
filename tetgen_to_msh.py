def convert_ele_node_to_msh(ele_file, node_file, output_msh_file):
    with open(ele_file, 'r') as ele:
        ele_lines = ele.readlines()

    with open(node_file, 'r') as node:
        node_lines = node.readlines()

    num_elements = int(ele_lines[0].strip().split()[0])
    num_nodes = int(node_lines[0].strip().split()[0])

    with open(output_msh_file, 'w') as msh:
        # Write MeshFormat
        msh.write("$MeshFormat\n")
        msh.write("2.2 0 8\n")
        msh.write("$EndMeshFormat\n")

        # Write Nodes
        msh.write("$Nodes\n")
        msh.write(f"{num_nodes}\n")
        for line in node_lines[1:num_nodes+1]:
            parts = line.strip().split()
            node_index = int(parts[0]) + 1  # Gmsh nodes start from 1
            x, y, z = parts[1], parts[2], parts[3]
            msh.write(f"{node_index} {x} {y} {z}\n")
        msh.write("$EndNodes\n")

        # Write Elements
        msh.write("$Elements\n")
        msh.write(f"{num_elements}\n")
        for line in ele_lines[1:num_elements+1]:
            parts = line.strip().split()
            element_index = int(parts[0]) + 1  # Gmsh elements start from 1
            nodes = [str(int(p) + 1) for p in parts[1:5]]  # Adjust node indices for Gmsh
            msh.write(f"{element_index} 4 0 {' '.join(nodes)}\n")
        msh.write("$EndElements\n")

# Example usage:
# convert_ele_node_to_msh('cube.ele', 'cube.node', 'output_cube.msh')

if __name__ == "__main__":
    import sys
    args = sys.argv[1:]
    path = args[0]
    ele_file = path + '.ele'
    node_file = path + '.node'
    output_msh_file = path + '.msh'
    convert_ele_node_to_msh(ele_file, node_file, output_msh_file)
