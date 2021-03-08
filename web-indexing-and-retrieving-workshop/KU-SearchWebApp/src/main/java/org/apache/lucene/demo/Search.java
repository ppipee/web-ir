package org.apache.lucene.demo;

import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.ScoreDoc;
import org.apache.lucene.search.TopDocs;

import java.io.IOException;
import java.util.Arrays;
import java.util.Comparator;

public class Search {
    public ScoreDoc[] getHits(IndexSearcher searcher, TopDocs result){
        ScoreDoc[] hits = result.scoreDocs;

        Arrays.sort(hits, new Comparator<ScoreDoc>() {
            @Override
            public int compare(ScoreDoc o1, ScoreDoc o2) {
                double score1 = 0, score2 = 0, omega = 0.5;
                try {
                    score1 = omega*o1.score + (1-omega)* Double.parseDouble(searcher.doc(o1.doc).get("PageRank"));
                } catch (IOException e) {
                    e.printStackTrace();
                }
                try {
                    score2 = omega*o2.score + (1-omega)* Double.parseDouble(searcher.doc(o2.doc).get("PageRank"));
                } catch (IOException e) {
                    e.printStackTrace();
                }

                if (score1 < score2) return 1;
                else if (score1 == score2) return 0;
                else return -1;
            }
        });

        return hits;
    }
}
