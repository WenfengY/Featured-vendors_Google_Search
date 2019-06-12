## Project: Footprint Improvement Umbrella

# Featured-vendors_Google_Search
## Featured vendors_Google_Search: python code and related document

Data driven leveraging Google Search API for strength of association - e.g. Netflix and AWS

**Goal:** using Google Web Search Page # Results to verify that which service provider (SP) is the primary one

**Idea:** to find a way to automate the capture of whenever a vendor / technology organization features a user organization.

**Steps:** 
1. identify standard customer pages on vendor (cloud service provider) companies' website to find customers, and form a list of 126 for 6 vendors (AWS, Azura, Google Could, Oracle Cloud, IBM Cloud, Alibaba Cloud)
2. using Python Library selenium as major tool for headless web searching tool to search and parse 
    the result pages, recoding search result # for 6 vendors
3. based on the #s for each customer, calculate the weights/percentages for all 6 vendors
    and pick the top one as the major SP for comparison
4.  Verify our hypothesis: the google search result page #s represent the SP association levels

5. To get conclusion


