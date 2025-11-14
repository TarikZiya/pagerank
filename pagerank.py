import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000

def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])    
    
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}"
              )
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory) -> dict[str, set[str]]:
    
    pages = dict()

    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]?)href=\"([^\"])\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor) -> dict[str, float]:

    return {_page: (1-damping_factor) / (len(corpus) -1) + (damping_factor / len(corpus[page]) if _page in corpus[page] else 0) for _page in corpus if page != _page}

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page b sampling n pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pagerank = {page: 0 for page in corpus}
    
    current_page = random.choice(list(corpus.keys()))
    pagerank[current_page] += 1
    
    for _ in range(n - 1):

        model = transition_model(corpus, current_page, damping_factor)
        
   
        pages = list(model.keys())
        probabilities = list(model.values())
        current_page = random.choices(pages, weights=probabilities, k=1)[0]
        
    
        pagerank[current_page] += 1
    
   
    pagerank = {page: count / n for page, count in pagerank.items()}
    
    return pagerank


def iterate_pagerank(corpus, damping_factor):
  
    n = len(corpus)
    
    
    pagerank = {page: 1 / n for page in corpus}
    
    
    corpus_copy = corpus.copy()
    for page in corpus_copy:
        if len(corpus_copy[page]) == 0:
            corpus_copy[page] = set(corpus.keys())
    
    convergence_threshold = 0.001
    
    while True:
        new_pagerank = {}
        
        for page in corpus:
        
            rank = (1 - damping_factor) / n
            
      
            for other_page in corpus:
                if page in corpus_copy[other_page]:
                    rank += damping_factor * (pagerank[other_page] / len(corpus_copy[other_page]))
            
            new_pagerank[page] = rank
        
       
        if all(abs(new_pagerank[page] - pagerank[page]) < convergence_threshold for page in corpus):
            break
        
        pagerank = new_pagerank
    
    return pagerank

if _name_ == "_main_":
    main()