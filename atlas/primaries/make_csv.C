#include <array>
#include <fstream>
#include <iostream>
#include <TBranch.h>
#include <TFile.h>
#include <TTree.h>

//---------------------------------------------------------------------------//
//! Usage: root make_csv.C
void make_csv()
{
    // Open ROOT file and load its "primaries" tree
    auto* file = TFile::Open("primaries_LArEndcapNeg0x6cd79ea0.root", "read");
    auto* primaries_tree = file->Get<TTree>("primaries");

    // Set up local variables associated to the root tree branches
    // Every time a tree->GetEntry(i) is called, these variables are overriden
    // by the value in the i-th entry in the branch it is associated with
    unsigned int event_id;
    int pdg;
    double energy;
    std::array<double, 3> pos;
    std::array<double, 3> dir;
    double time;

    // Associate the local variables above to their respective branches
    primaries_tree->SetBranchAddress("event_id", &event_id);
    primaries_tree->SetBranchAddress("particle", &pdg);
    primaries_tree->SetBranchAddress("energy", &energy);
    primaries_tree->SetBranchAddress("pos", &pos);
    primaries_tree->SetBranchAddress("dir", &dir);
    primaries_tree->SetBranchAddress("time", &time);


    std::ofstream out("primaries_LArEndcapNeg0x6cd79ea0.csv");

    // Loop over all entries in the tree; Each entry is one particle
    for (auto i = 0; i < primaries_tree->GetEntries(); ++i)
    {
        primaries_tree->GetEntry(i);
        //std::cout << "---------- Entry " << i << " ----------" << std::endl;
        //std::cout << "Event ID : " << event_id << std::endl;
        //std::cout << "PDG      : " << pdg << std::endl;
        //std::cout << "Energy   : " << energy << std::endl;
        //std::cout << "Position : " << pos[0] << ", " << pos[1] << ", "
        //          << pos[2] << std::endl;
        //std::cout << "Direction: " << dir[0] << ", " << dir[1] << ", "
        //          << dir[2] << std::endl;
        //std::cout << "Time     : " << time << std::endl;

        out << pos[0] << ", " << pos[1] << "," << pos[2] << "\n";
    }

    // Close the file explicitly if needed
    // ROOT should close the file correctly when it goes out of scope through
    file->Close();
}
