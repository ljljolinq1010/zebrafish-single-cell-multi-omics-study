The repository contains scripts and data from the study: "Dissecting the Regulatory Logic of Specification and Differentiation during Vertebrate Embryogenesis"

1. scenicplus.ipynb notebook is used to reconstruct gene regulatory networks using the SCENIC+ pipeline
   
2. folder data:
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
     example.ipynb
   
