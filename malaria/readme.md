Creating a folder called **`malaria/`**,and in the `malaria/` creating two sub-directory called **`Haemoproteus_Data/`** and **`prediction/`**    

# Plasmodium data
In the folder `prediction` 
Copy the data of malaria
```
cp /home2/resources/binp29/Data/malaria/plasmodiumGenomes.tgz .
tar -xvzf plasmodiumGenomes.tgz
```
copy the data of prediction of malaria
```
cp /tmp/Prediction/*.gtf .
```

# Processing of Haemoproteus tartakovskyi data
In this chapter, we operate in the folder `Haemoproteus_Data`  
copy the file `Haemoproteus_tartakovskyi.genome` from course folder into this file  
```
cp /resources/binp29/Data/malaria/Haemoproteus_tartakovskyi.genome.gz . 

gunzip Haemoproteus_tartakovskyi.genome.gz
```
## Clean genome sequence
Select an appropriate GC-content (30%) and remove scaffolds above this threshold.   
Also remove scaffolds that are less than 3000 nucleotides.  
```
cp /resources/binp29/Data/malaria/removeScaffold.py .
python removeScaffold.py Haemoproteus_tartakovskyi.genome 30 Haemoproteus_tartakovskyi.fna 3000
```
Using the python file to finish the removal.   
The input file is `Haemoproteus_tartakovskyi.genome`, and the output file is `Haemoproteus_tartakovskyi.fna`   

## Make a gene prediction
### With the new genome file, make a gene prediction, using `gmes_petap.pl` .
```
nohup gmes_petap.pl --ES --sequence Haemoproteus_tartakovskyi.fna --min_contig 5000 &
```
the output file is `genemark.gft`, here we change the name into `Haemoproteus_tartakovskyi.gtf`.    

### Running the **`gffParse.pl`** to get a new fasta file.  
**Firstly, setting the `.bashrc`**    
open the bin folder, copy the software `gffParse.pl` into bin foder    
```
cp /resources/binp29/Programs/gffParse.pl .  
```
go to the home directory, change bashrc path    
```
cd   
nano .bashrc  
#edit the file  
export PATH=$PATH:~/local/bin/  
#close and save  
source .bashrc  
```
**Running the `gffParse.pl`**
The **input** file here is the filtered fasta file `Haemoproteus_tartakovskyi.fna`, and `Haemoproteus_tartakovskyi.gtf`.    
```
perl ~/bin/gffParse.pl -i Haemoproteus_tartakovskyi.fna -g Haemoproteus_tartakovskyi.gtf -p -c  
```
But, first running, it would get the error, because in gtf file `Haemoproteus_tartakovskyi.gtf`, the structure of first column mismatches the header of fasta file (input)  
Then we modify the gtf file, and output the result into file `Ht2.gff`.      
```
cat Haemoproteus_tartakovskyi.gtf | sed "s/ GC=.*\tGeneMark.hmm/\tGeneMark.hmm/" > Ht2.gff  
```
**Rerun the `gffParse.pl`**  
```
perl ~/bin/gffParse.pl -i Haemoproteus_tartakovskyi.fna -g Ht2.gff -p -c -F  
```
The **output file** are `gffParse.faa` and `gffParse.fna`.    
### BLAST 
create the link from database  
```
echo $BLASTDB  
ln -s /resources/binp29/Data/malaria/taxonomy.dat taxonomy.dat  
ln -s /resources/binp29/Data/malaria/uniprot_sprot.dat uniprot_sprot.dat  
```
Copy the blast output file and python file for parsing from course server.    
```
cp /resources/binp29/Data/malaria/backup_results/Ht.blastout.gz .  
gunzip Ht.blastout.gz
cp /resources/binp29/Data/malaria/datParser.py .  
```
Using the python file `datParser.py` to find the scaffold of bird, the **input** file is `gffParse.fna` and **output** the headers into a txt file `scaffolds.txt`    
```
python datParser.py Ht.blastout gffParse.fna taxonomy.dat uniprot_sprot.dat > scaffolds.txt  
```
### using python to remove scaffolds abput bird  
I operate this step in my window system
copy the input file and python script into windows system and run python script `Parse_bird.py`

python script: `Parse_bird.py`    
input file: `Haemoproteus_tartakovskyi.fna`  
output file: `gffParse_no_bird.fna`  

Finally, moving the output file `gffParse_no_bird.fna` back to cource server folder `Haemoproteus_Data/` 

### make the prediction again  
in **input** file is `gffParse_no_bird.fna`, and the **output** file is `genemark.gtf`.
`nohup gmes_petap.pl --ES --sequence gffParse_no_bird.fna --min_contig 5000 --cores 10 &`  
### Getting the fastafile, 
firstly, modify the gft file `genemark.gtf`, getting output file `Ht.gff`
`cat genemark.gtf | sed "s/ GC=.*\tGeneMark.hmm/\tGeneMark.hmm/" > Ht.gff`
Then we run `gffParse.pl`, **input** `gffParse_no_bird.fna` and `Ht.gff`, **output** `Ht.faa` `Ht.fna` `Ht.log`   
`perl ~/bin/gffParse.pl -i gffParse_no_bird.fna -g Ht.gff -p -c -b Ht`

# Create the tree
The operation of this chapter are in **folder `prediction/`**
## Identify orthologs
### print protein sequence in fasta format  
Firstly, copy the file `Ht.faa` from `Haemoproteus_Data/` into `prediction/`
Then copy `Tg.gff.gz` from the course directory.
```
cp malaria/Haemoproteus_Data/Ht.faa .
cp /resources/binp29/Data/malaria/Tg.gff.gz .
gunzip Tg.gff.gz 
```
Then running the `gffParse.pl`
```
perl ~/bin/gffParse.pl -i Plasmodium_yoelii.genome -g plasmodium_yoelii.gtf -p -c -b Py
perl ~/bin/gffParse.pl -i Plasmodium_vivax.genome -g plasmodium_vivax.gtf -p -c -b Pv
perl ~/bin/gffParse.pl -i Plasmodium_faciparum.genome -g plasmodium_faciparum.gtf -p -c -b Pf
perl ~/bin/gffParse.pl -i Plasmodium_cynomolgi.genome -g plasmodium_cynomolgi.gtf -p -c -b Pc
perl ~/bin/gffParse.pl -i Plasmodium_berghei.genome -g plasmodium_berghei.gtf -p -c -b Pb
perl ~/bin/gffParse.pl -i Plasmodium_knowlesi.genome -g knowlesi.gtf -p -c -b Pk
perl ~/bin/gffParse.pl -i Toxoplasma_gondii.genome -g Tg.gff -p -c -b Tg
```
There are eight `.faa` file now.
#### installing `proteinortho` and `busco`
```
bash Miniconda3-py39_4.11.0-Linux-x86_64.sh
source .bashrc
conda config --add channels defaults
conda config --add channels bioconda
conda config --add channels conda-forge
conda install proteinortho
conda update conda
conda install -c bioconda -c conda-forge busco=5.3.0
conda update proteinortho
```
#### run the `proteinortho6.pl` `busco`
```
nohup proteinortho6.pl {Ht,Pb,Pc,Pf,Pk,Pv,Py,Tg}.faa &
for file in Ht Pb Pc Pf Pk Pv Py Tg; do busco -i $file.faa -o $file -m prot -l apicomplexa;done
```


















