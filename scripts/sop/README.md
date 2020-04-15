# Downloading Wikipedia Corpus

We use the preprocessing code from https://github.com/NVIDIA/DeepLearningExamples/tree/master/PyTorch/LanguageModeling/BERT#getting-the-data
and the bash scripts provided here is used to help with streamlining the data generation in the NVIDIA repository.

First, git clone https://github.com/NVIDIA/DeepLearningExamples.git.
Then, move create_wiki_data.sh and get_small_english_wiki.sh into DeepLearningExamples/PyTorch/LanguageModeling/BERT/data.

Then, follow the instructions below:

The data creation for SOP is almost the same as MLM, except you need to edit the following.
In `DeepLearningExamples/PyTorch/LanguageModeling/BERT/data/TextSharding.py`, replace line 55:
`self.articles[global_article_count] = line.rstrip()` with `self.articles[global_article_count] = line.rstrip() + "\n ========THIS IS THE END OF ARTICLE.========"`.
This is because SOP requires a signal for the end of each Wikipedia article.

Run `bash create_wiki_sop_data.sh $lang $save_directory`
The NVIDIA code supports English (en) and Chinese (zh) wikipedia.

For example, to download and process English Wikipedia and save it in `~/Download` directory, run
`bash create_wiki_sop_data.sh en ~/Download`

The above command will download the entire English Wikipedia.

In our experiments, we only use a small subset (around 5% of) the entire English Wikipedia, which has the same number of sentences as Wikitext103.
To get this subset, run `bash get_small_english_wiki.sh $path_to_wikicorpus_en`. where $path_to_wikicorpus_en is the directory where you saved the full processed `wikicorpus_en` corpus.
