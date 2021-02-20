---
title: Notes on Proppy
author: Zubair Abid
linkcolor: blue
---

Analysis done on [google colab].

# Proppy's Data Format

This is based on a glance at the dataset itself, and not whatever is written on
the zenodo entry.

1. Article Text
2. Location of the article
3. "Average Tone"
4. Article date
5. GDELT Article ID
6. Article URL
7. Article Author
8. Article Title
9. MBFC Factuality label [^invest_9] [^ood_9]
10. MBFC URL to Publication
11. Publication Name
12. MBFC notes on the Publication
13. MBFC bias label
14. Publication domain URL
15. **Propaganda label**: 1 is Propaganda, -1 isn't.

# Looking into it

- **Number of articles with MBFC available:** 19631/35986.

  This isn't perfect. In a random sample, at least two articles from CNN were
  found -- one labelled correctly as "CNN" and the other as "cnn.com", so the
  latter did not have the label attached to it. Eg: "Freedom Outpost" is listed
  correctly 54% of the time.

  Probably does not matter for
  propaganda scores, as non-listed sources can also be propaganda. If we need to
  correlate MBFC to it however this is an issue. **This might be resolvable by
  looking at Publication domain URL.**

  There are positive propaganda scores associated with unknown sources on MBFC.
  Example: vdare.com, GDELT ID: 758670980, Row ID: 33946. Another example is a
  mis-done entry of frontpagemag.

  Should clarify that not all "unknown" is incorrectly tagged~~; something like
  "Freedom Outpost" is actually not in MBFC (and is considered propaganda in the
  two random samples it was seen in).~~ The Washington Standard is an example.
- **Number of articles tagged as "propaganda":** 4021/35986. 

  Need to investigate: are all articles from a source called propaganda? Is it
  true the other way round? A quick check on "Freedom Outpost" seems to indicate
  the former.

  Yes. That is the case. There are 10 sources always classified as propaganda,
  and 159 others that are never.
- **Number of sources classified as propaganda:** 10/169
- **Checking propaganda+ sources against MBFC ratings:**

  This information was checked against MBFC as it is on the website on the 21st 
  of February, and not on the Proppy dataset (which has it slightly 
  out-of-date).

  | Source                  | Factuality Label | Bias Label             | Link                                                   |
  |-------------------------|------------------|------------------------|--------------------------------------------------------|
  | Breaking 911            | Very Low         | -                      | <https://mediabiasfactcheck.com/breaking911/>          |
  | SHTFPlan                | Mixed            | Extreme Right          | <https://mediabiasfactcheck.com/shtfplan-com/>         |
  | Clash Daily             | Low              | Extreme Right          | <https://mediabiasfactcheck.com/clash-daily/>          |
  | Personal Liberty        | Low              | Extreme Right          | <https://mediabiasfactcheck.com/personal-liberty/>     |
  | Frontpage Magazine      | Low              | Extreme Right [^diff]  | <https://mediabiasfactcheck.com/frontpage-magazine/>   |
  | The Washington Standard | -                | -                      | -                                                      |
  | VDare                   | Low              | Extreme Right [^diff]  | <https://mediabiasfactcheck.com/vdare/>                |
  | Freedom Outpost         | - [^frmb]        | -                      | <https://mediabiasfactcheck.com/fake-news/>            |
  | Remnant                 | Low              | Extreme Right          | <https://mediabiasfactcheck.com/the-remnant-magazine/> |
  | Lew Rockwell            | Mixed            | Extreme Right [^diff1] | <https://mediabiasfactcheck.com/lew-rockwell/>         |

- **Checking MBFC Bias labels against Factuality labels**
 
  This will be using the Proppy MBFC Labels, I guess.

  It appears that anything that is Low or under on MBFC is considered to be 
  propaganda. SHTFPlan and Lew Rockwell don't follow this rule, but their 
  factuality scores might have changed since Proppy was compiled -- we've seen 
  others have.

  The table below is compiled using Proppy's MBFC labels. The bias is more
  coarse-grained than the actual labels as they do not make sense in any 
  publication related to the dataset.

  | Label         | Number | High | Mixed | Low/Very Low | NIL | unknown |
  |---------------|--------|------|-------|--------------|-----|---------|
  | NIL           | 14     | 9    | 2     | 3            | 0   | 0       |
  | unknown       | 65     | 0    | 0     | 0            | 0   | 65      |
  | extreme right | 6      | 0    | 1     | 5            | 0   | 0       |
  | right         | 8      | 3    | 3     | 2            | 0   | 0       |
  | right center  | 6      | 5    | 1     | 0            | 0   | 0       |
  | least biased  | 7      | 7    | 0     | 0            | 0   | 0       |
  | left center   | 60     | 56   | 3     | 0            | 1   | 0       |
  | left          | 3      | 1    | 2     | 0            | 0   | 0       |

  **Basically**: Using NELA-GT will be useless as it is also basing its 
  factuality on the MBFC labels, and as we can see here there is an easily
  detectable correlation between specific biases and low factuality.

[^invest_9]: This is definitely the case, I checked against the entry for the
Hartford Courant, Arab News, SHTFPlan, Frontpage Magazine, Korea Herald.

[^ood_9]: This is also out of date. Arab News is marked as "HIGH", but it is
currently on "MIXED" on the website. Also for SHTFPlan, the label is "MIXED" but
the reasoning is given instead. This is also the case for Frontpage Magazine.
For Korea Herald this is not the case as there is not reasoning given. In
general, the reasoning is not given in non-propaganda -- probably means that
proppy's reasoning for propaganda is the MBFC reasoning.

[^frmb]: It is not on the site, but is listed under ["Questionable Sources"]. 
On the other hand, you can see the data in the Proppy dataset itself.

[^diff]: On proppy, this is just "Right"

[^diff1]: On proppy, this is "NIL"

[google colab]: https://colab.research.google.com/drive/1SoTOoZXGESGs9AU26CIvxgwNxtwcUMxk#scrollTo=MdoHuxMG552Q

["Questionable Sources"]: https://mediabiasfactcheck.com/fake-news/
