# Snort
## Description
Snort regular expressions are built from Snort snapshot 2.9.7.0 October 13th 2009.

Regexes from the following files were used to create the 1chip ANMLZoo standard candle benchmark. Only regexes that don't contain quantifiers and also successfully compile using the AP SDK were used.

deleted.regex 
app-detect.regex 
browser-chrome.regex 
file-identify.regex 
exploit-kit.regex 
browser-ie.regex 
file-other.regex 
os-windows.regex 
server-mail.regex 
server-webapp.regex 
pua-adware.regex 


Inputs were taken from the following repository:
https://download.netresec.com/pcap/ists-12/2015-03-08/

Evaluation inputs were derived from snort.log.1425823194.

## Inputs
### snort_1MB.input
### snort_10MB.input

## References
Roesch, Martin. "Snort: Lightweight Intrusion Detection for Networks." LISA. Vol. 99. No. 1. 1999.
