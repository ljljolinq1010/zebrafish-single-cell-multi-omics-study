The repository contains scripts and data from the study: "Dissecting the Regulatory Logic of Specification and Differentiation during Vertebrate Embryogenesis"

1. This tutorial provides step-by-step instructions on how to use scMultiome data to perform the following analyses:
   
   The tutorial is here: https://ljljolinq1010.github.io/zebrafish-single-cell-multi-omics-study/tutorial_scMultiome.html
   
   The scMultiome data is here: https://drive.google.com/file/d/1qQGUSENjQ0ohZDtvcnejS6XKS0H0HrCW/view?usp=drive_link

   A. Identify putative enhancers for genes of interest
   
   B. Plot gene expression, chromatin accessibility, and the association score for genes of interest
   
   C. Idnetify the transcription factor binding site for the peaks of interest through motif scaning
   
   D. Motif entichment analysis for cell type specific peaks
   



   
3. folder data:

   A. eRegulon.txt: contains eRegulon information
   
   B. eRegulon_specificity_score.txt: contains the specificty score of each eRegulon in each cell state
   
   C. highToSomite_peaks.txt: contains the genome coordinates of all ATAC peaks
   
   D. singleCell_meta_data.txt: contaisn the per-cell metadata information
   
   E. Seurat object of the nine-stage integrated single-cell multi-omic datasets saved in:
   
      https://drive.google.com/drive/folders/1NTRCoIOviDVmsVhDiaPXpbdDqs40D7rz?usp=drive_link
   
   F. DeepDanio identified motifs and TFBSs for each of the 95 cell states saved in:
   
      https://drive.google.com/drive/folders/1kRCzl9ZrZpTpb-Jf1-dalV5FD6lVFTN1?usp=drive_link 




4. folder DeepDanio:

    A. it contains three deep learning models
   
     DeepDanio/resnet_chr_split_0_w_mse_0.5_w_pearsonr_0.5_continued.h5
   
     DeepDanio/resnet_chr_split_1_w_mse_0.5_w_pearsonr_0.5_continued.h5
   
     DeepDanio/resnet_chr_split_2_w_mse_0.5_w_pearsonr_0.5_continued.h5
   
   B. it cotains example code for predicting chromatin accessibility based on DNA sequences
  
     "example.ipynb"
   
