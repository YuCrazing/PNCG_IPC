#include <iostream>
#include <fstream>
#include <unordered_map>
#include <vector>
#include <array>
#include <set>
#include <algorithm>

using Triangle = std::array<int, 3>;
using Tetrahedron = std::array<int, 4>;

struct TriangleHash {
    size_t operator()(const Triangle& tri) const {
        Triangle sorted_tri = tri;
        std::sort(sorted_tri.begin(), sorted_tri.end());
        return std::hash<int>()(sorted_tri[0]) ^ std::hash<int>()(sorted_tri[1]) ^ std::hash<int>()(sorted_tri[2]);
    }
};

void extractSurfaceFaces(const std::string& eleFilename, const std::string& faceFilename) {
    std::ifstream eleFile(eleFilename);
    if (!eleFile) {
        std::cerr << "Unable to open input file: " << eleFilename << std::endl;
        return;
    }

    int numTetrahedra, verticesPerTet, dummy;
    eleFile >> numTetrahedra;

    std::vector<Tetrahedron> tets(numTetrahedra);
    for (int i = 0; i < numTetrahedra; ++i) {
        eleFile >> dummy >> tets[i][0] >> tets[i][1] >> tets[i][2] >> tets[i][3];
    }
    eleFile.close();

    std::unordered_map<Triangle, int, TriangleHash> faceCount;

    for (const auto& tet : tets) {
        Triangle faces[4] = {
            {tet[0], tet[1], tet[2]},
            {tet[0], tet[1], tet[3]},
            {tet[0], tet[2], tet[3]},
            {tet[1], tet[2], tet[3]}
        };

        for (const auto& face : faces) {
            Triangle sorted_face = face;
            std::sort(sorted_face.begin(), sorted_face.end());
            faceCount[sorted_face]++;
        }
    }

    std::vector<Triangle> surfaceFaces;
    for (const auto& pair : faceCount) {
        if (pair.second == 1) { // Boundary face
            surfaceFaces.push_back(pair.first);
        }
    }

    std::ofstream faceFile(faceFilename);
    if (!faceFile) {
        std::cerr << "Unable to open output file: " << faceFilename << std::endl;
        return;
    }

    faceFile << surfaceFaces.size() << " 3 0\n";
    for (size_t i = 0; i < surfaceFaces.size(); ++i) {
        faceFile << (i) << " "
                 << surfaceFaces[i][0] << " "
                 << surfaceFaces[i][1] << " "
                 << surfaceFaces[i][2] << "\n";
    }

    faceFile.close();

    std::cout << "Extracted " << surfaceFaces.size() << " surface faces to " << faceFilename << std::endl;
}

int main(int argc, char** argv) {
    if (argc != 3) {
        std::cerr << "Usage: " << argv[0] << " input.ele output.face" << std::endl;
        return 1;
    }

    extractSurfaceFaces(argv[1], argv[2]);

    return 0;
}
