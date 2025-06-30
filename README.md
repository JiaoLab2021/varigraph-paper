# **Varigraph: an accurate and widely applicable pangenome graph-based variant genotyper for diploid and polyploid genomes**

## This page documents the ​​code and command-line usage​​ for the genome graph software evaluated in our Varigraph study. We benchmarked eight widely-used tools in the field, including:

 - [VG-MAP][VG_url]
 - [VG-Giraffe][VG_url]
 - [GraphAligner][GraphAligner_url]
 - [Paragraph][Paragraph_url]
 - [BayesTyper][BayesTyper_url]
 - [GraphTyper2][GraphTyper2_url]
 - [PanGenie][PanGenie_url]
 - [GATK][GATK_url]
 - [Freebayes][Freebayes_url]
 - [Octopus][Octopus_url]

[VG_url]: https://github.com/vgteam/vg
[GraphAligner_url]: https://github.com/maickrau/GraphAligner
[Paragraph_url]: https://github.com/Illumina/paragraph
[BayesTyper_url]: https://github.com/bioinformatics-centre/BayesTyper
[GraphTyper2_url]: https://github.com/DecodeGenetics/graphtyper
[PanGenie_url]: https://github.com/eblerjana/pangenie
[GATK_url]: https://github.com/broadinstitute/gatk
[Freebayes_url]: https://github.com/freebayes/freebayes
[Octopus_url]: https://github.com/luntergroup/octopus

## 1. ​​Code for Genotyping​​:

### VG MAP

To begin, the initial step involves building a genome graph and creating index:

```shell
# vg autoindex
vg autoindex -T ./temp/ -M 50G -t 10 -R XG --workflow map -r refgenome.fa -v input.vcf.gz -p sample
# vg snarls
vg snarls -t 10 sample.xg 1>sample.snarls
```

Next, the sequencing reads are aligned to the graph:

```shell
# vg map
vg map -t 10 -g sample.gcsa -x sample.xg -f read.1.fq.gz -f read.2.fq.gz 1>sample.gam
```

Finally, genotyping the variants in the graph using the `sample.gam` file:

```shell
# vg pack
vg pack -t 10 -x sample.xg -g sample.gam -o sample.pack
# vg call
vg call -t 10 -s sample sample.xg -k sample.pack -r sample.snarls 1>sample.vcf
```

### VG Giraffe

Similar to `VG MAP`, the initial step involves building a genome graph and creating index:

```shell
# vg autoindex
vg autoindex -T ./temp/ -M 50G -t 10 -R XG --workflow giraffe -r refgenome.fa -v input.vcf.gz -p sample
# vg snarls
vg snarls -t 10 sample.xg 1>sample.snarls
```

Next, the sequencing reads are aligned to the graph:

```shell
# vg giraffe
vg giraffe -t 10 -x sample.xg -Z sample.giraffe.gbz -m sample.min -d sample.dist -f read.1.fq.gz -f read.2.fq.gz 1>sample.gam
```

Finally, genotyping the variants in the graph using the `sample.gam` file:

```shell
# vg pack
vg pack -t 10 -x sample.xg -g sample.gam -o sample.pack
# vg call
vg call -t 10 -s sample sample.xg -k sample.pack -r sample.snarls 1>sample.vcf
```

### GraphAligner

Similar to `VG MAP`, the initial step involves building a genome graph and creating index:

```shell
# vg construct
vg construct -t 10 -r refgenome.fa -v input.vcf.gz 1>sample.vg
# vg index
vg index -t 10 -x sample.xg sample.vg
# vg snarls
vg snarls -t 10 sample.xg 1>sample.snarls
```

Next, the sequencing reads are aligned to the graph:

```shell
# GraphAligner
GraphAligner -t 10 -g sample.vg -x vg -f read.1.fq.gz -f read.2.fq.gz -a sample.gam
```

Finally, genotyping the variants in the graph using the `sample.gam` file:

```shell
# vg pack
vg pack -t 10 -x sample.xg -g sample.gam -o sample.pack
# vg call
vg call -t 10 -s sample sample.xg -k sample.pack -r sample.snarls 1>sample.vcf
```

### Paragraph

The required input files for [Paragraph][Paragraph_url] include a reference genome, a VCF file, and a configuration file that specifies the path path to BAM file. The configuration file format is specified below:

```shell
# sample.txt
id      path      depth     read length
sample     sample.bam   30        150
```

To genotype the variants, execute the command provided below:

```shell
# genotyping
multigrmpy.py -i input.vcf.gz -m sample.txt -r refgenome.fa --threads 10 -M 600 -o sample
```

### GraphTyper2

To run [GraphTyper2][GraphTyper2_url], you will need to provide the following input files: a reference genome, a VCF file, a BAM file, coverage files for the BAM, and region files specifying the regions to be genotyped.

The BAM coverage file can be generated using the following command:

```shell
# samtools
samtools idxstats sample.bam | head -n -1 | awk '{sum+=$3+$4; ref+=$2} END{print sum/ref}' 1>sample.cov
```

The region file should follow this format:

```shell
# region.txt
chr1:1-30200790
chr2:1-45040766
...
```

To genotype the variants, execute the command provided below:

```shell
# genotyping
graphtyper genotype_sv refgenome.fa input.vcf.gz --sam=sample.bam --region_file=region.txt --sampleput=sample --avg_cov_by_readlen=sample.cov
```

### BayesTyper

To run [BayesTyper][BayesTyper_url], you will need to provide the following input files: a reference genome, a VCF file, a BAM file, and sample file hat specifies the prefix used by [bayesTyperTools' makeBloom tool][BayesTyper_url].

The sample file should follow this format:

```shell
# sample.tsv
sample F sample.bam
```

Before running [BayesTyper][BayesTyper_url], it is necessary to use [KMC][KMC_url] to count the k-mers in the BAM file.

```shell
# KMC
kmc -k55 -ci1 -t1 -fbam sample.bam sample.bam sample.bam
```

Based on the generated k-mers, use [bayesTyperTools makeBloom][BayesTyper_url] to construct a read Bloom filter.

```shell
# bayesTyperTools makeBloom
bayesTyperTools makeBloom -k sample.bam -p 10
```

Then, use [bayesTyper cluster][BayesTyper_url] for variants clustering.

```shell
# bayesTyper cluster
bayesTyper cluster -v input.vcf.gz -s sample.tsv -g refgenome.fa -p 10
```

Finally, use [bayesTyper cluster][BayesTyper_url] for genotyping.

```shell
# bayesTyper cluster
for i in $(ls | grep 'bayestyper_unit_'); do
	bayesTyper genotype -v $i/variant_clusters.bin -c bayestyper_cluster_data -s sample.tsv -g refgenome.fa -o $i/bayestyper -z -p 10 --noise-genotyping
done
```

### PanGenie

Running [PanGenie][PanGenie_url] requires only one simple command. However, as [PanGenie][PanGenie_url] cannot recognize compressed files, the first step is to decompress the input file before genotyping.

```shell
# decompress
gunzip input.vcf.gz
gunzip read.1.fq.gz
gunzip read.2.fq.gz
cat read.1.fq read.2.fq > sample.fq
# PanGenie
PanGenie -s sample -i sample.fq -r refgenome.fa -v sample.vcf -t 10 -j 10 -o sample
```

### GATK

Running [GATK][GATK_url] requires only one simple command.

```shell
# GATK
gatk HaplotypeCaller \
    --native-pair-hmm-threads 4 \
    -R refgenome.fa \
    -I sample.bam \
    --sample-ploidy 4 \
    -O sample.vcf.gz
```

### Freebayes

Running [Freebayes][Freebayes_url] requires only one simple command.

```shell
# Freebayes
freebayes -T 32 -f refgenome.fa -p 4 sample.bam 1>sample.vcf 2>log.txt &
```

### Octopus

Running [Octopus][Octopus_url] requires only one simple command.

```shell
# Octopus
octopus -R refgenome.fa -I sample.bam -o sample.vcf.gz --threads 32 -P 4
```

## 2. ​​Code for Plotting:

### All plotting code has been uploaded to the draw folder.

You can run the Python scripts directly to generate the plots.

Sample data and code are included — no additional setup is needed.
