.. _label-wos:

WoS Preparation
==========================

Our implementation of bibliometrics tools require data to be in a Pandas dataframe format and that column names match the WoS tags (TI for title, TC for the citations, ...).  

To meet those requirements, we suggest using the package Bibliometrix on R. For step-by-step explications, see their `tutorial <https://www.bibliometrix.org/vignettes/Introduction_to_bibliometrix.html>`_. Basically, text files can be downloaded from the `Web of Science website <http://www.webofknowledge.com>`_ and the package bibliometrix can create a dataframe by parsing those files. A dataframe can easily be exported as a CSV (Comma Separated Values) file and used with our library pyBiblio. 

There exists several other libraries in different programming languages that can also parse WoS text files. As long as WoS tags are preserved, any method can be used to prepare your data.
