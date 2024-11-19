The repository contains tutorials, scripts, and data from the study: "Dissecting the Regulatory Logic of Specification and Differentiation during Vertebrate Embryogenesis"

1. scMultiome tutorial: this tutorial provides step-by-step instructions on how to use scMultiome data to perform the following analyses:
   
   A. Identify putative enhancers for genes of interest
   
   B. Plot gene expression, chromatin accessibility, and their association scores for genes of interest
   
   C. Idnetify the transcription factor binding site for the peaks of interest through motif scaning
   
   D. Motif entichment analysis for cell type specific peaks

   The tutorial is here: https://ljljolinq1010.github.io/zebrafish-single-cell-multi-omics-study/tutorial_scMultiome.html
   
   The scMultiome data is here: https://drive.google.com/file/d/1qQGUSENjQ0ohZDtvcnejS6XKS0H0HrCW/view?usp=drive_link

2. SCENIC+ tutorial: this tutorial provides step-by-step instructions on using scMultiome data to reconstruct gene regulatory networks with the SCENIC+ pipeline

   The tutorial is here: https://ljljolinq1010.github.io/zebrafish-single-cell-multi-omics-study/tutorial_SCENIC+.html
   
   
3. DeepDanio tutorial: this tutorial provides step-by-step instructions on using DeepDanio to perform the following analyses:
   
   A. Predict the chromatin accessibility of a given 500 bp DNA sequence across 95 different cell states during zebrafish embryogenesis
   
   B. Calculate and visualize the contribution score for each nucleotide in the given sequence across any of the 95 cell states

   The tutorial is here: https://ljljolinq1010.github.io/zebrafish-single-cell-multi-omics-study/DeepDanio/tutorial_DeepDanio.html
 
4. Folder data:

   A. eRegulon.txt: contains eRegulon information
   
   B. eRegulon_specificity_score.txt: contains the specificty score of each eRegulon in each cell state
   
   C. highToSomite_peaks.txt: contains the genome coordinates of all ATAC peaks
   
   D. singleCell_meta_data.txt: contaisn the per-cell metadata information
   
   E. Seurat object of the nine-stage integrated single-cell multi-omic datasets saved in:
   
      https://drive.google.com/drive/folders/1NTRCoIOviDVmsVhDiaPXpbdDqs40D7rz?usp=drive_link
   
   F. DeepDanio identified motifs and TFBSs for each of the 95 cell states saved in:
   
      https://drive.google.com/drive/folders/1kRCzl9ZrZpTpb-Jf1-dalV5FD6lVFTN1?usp=drive_link 

5. Folder DeepDanio:

    A. It contains three DeepDanio models
   
     DeepDanio/resnet_chr_split_0_w_mse_0.5_w_pearsonr_0.5_continued.h5
   
     DeepDanio/resnet_chr_split_1_w_mse_0.5_w_pearsonr_0.5_continued.h5
   
     DeepDanio/resnet_chr_split_2_w_mse_0.5_w_pearsonr_0.5_continued.h5
   
   B. It contains the scripts that support the DeepDanio tutorial
   
