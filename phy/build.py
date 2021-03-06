import os, sys, glob, shutil

d = os.environ['HOME']
if len(sys.argv) == 1 :
    os.system("pdfunite \
    phy_basics/phy_basics.pdf \
    phy_lagrange/phy_lagrange.pdf \
    phy_hamiltonian/phy_hamiltonian.pdf \
    phy_dblpend/phy_dblpend.pdf \
    phy_control_1/phy_control_1.pdf \
    phy_control_3/phy_control_3.pdf \
    phy_varcalc/phy_varcalc.pdf \
    " + d + "/Downloads/phy.pdf" \
    )
    exit()
    
elif sys.argv[1] == 'all':
    for a in sorted(glob.glob("pny*")):
        os.chdir(a)
        os.system("pdflatex -shell-escape %s" % glob.glob("phy_*.tex")[0] )
        os.chdir("..")
        
    
elif sys.argv[1] == 'clean':
    os.system("find . -name '_region_*' | xargs rm  -rf")
    os.system("find . -name '_minted-*' | xargs rm  -rf")
            
elif sys.argv[1] == 'tex':
    file = glob.glob('phy_*.tex')
    os.system("pdflatex -shell-escape %s" % file[0])
    d = "/data/data/com.termux/files/home/storage/downloads"
    if os.path.isdir(d):
        ff = file[0].replace(".tex",".pdf")
        shutil.copy(ff,d)
    
