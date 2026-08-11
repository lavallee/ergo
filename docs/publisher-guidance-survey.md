# Publisher guidance: how often it exists, and where it hides

A sample of twenty widely used open datasets (surveyed 2026-08), asking one
question: does the publisher ship non-data guidance alongside the data — a
notes tab, a readme, a cover page, an errata list, a technical manual, a data
dictionary with caveats — and could a program holding only the download URL
ever find it?

Everything below was read from the publisher's own page, file, or API. Where a
sentence is quoted, it was retrieved literally from the URL given. Three
sources refused automated clients entirely (`www.bls.gov`, `www.bts.gov`,
`transit.dot.gov` all return 403 to curl, to a plain fetcher, and to a real
headless browser); those gaps are recorded rather than filled.

**The headline: guidance is not rare. It is nearly universal, it is usually
the part that changes an honest claim, and it is usually somewhere the
download does not point.**
Nineteen of twenty publishers ship something. Eighteen of twenty ship at least
one sentence that constrains what a reader may honestly claim. But only seven
put that sentence anywhere a fetcher would encounter without being told to go
looking.

---

## 1. Guidance that travels with the data

Seven datasets put a caveat inside — or immediately beside — the thing you
download. This is the minority case, and it is the only case where a cold
reader cannot miss it.

**NJ Department of Education — School Performance Reports, 2020-21 database**
([download page](https://www.nj.gov/education/spr/download/)). The workbook
`Database_SchoolDetail.xlsx` has 63 sheets. Sheet 1 of 63 is named `Important
2020-2021 Notes` (Excel truncates at 31 characters); its cell A1 carries the
full heading, *Important 2020-2021 Notes - Please Read Before Using Data in
this Database*. The sheet is a status table — 40 report sections, each marked
"no known systematic issues", "there may be some impact as a result of
COVID-19", or "Data is not available". Cell A1:

> "For all these reasons, we encourage school communities, this year more than
> ever, to reach out to their districts to see how COVID-19 may have impacted
> the data for their district and use caution in comparing data in the
> 2020-2021 School Performance reports to prior or future years."

Cell D25, on chronic absenteeism, is more specific: *"because the number of
days students spent in in-person and remote learning environments during the
school year differed, the NJDOE recommends caution in comparing 2020-2021
attendance data between schools and districts and to prior or future school
years."* Five data families — NJSLA participation and performance, student
growth, progress toward English proficiency, ESSA summative ratings, status
against annual targets — are simply absent from the file. **Honest-say caveat:
yes**, on three axes at once (universe change, comparability break, definition
change: a new graduation pathway, *"Requirements waived under Executive Order
214"*). **Discovery: the tab is unmissable once you have the file — but the
file is hard to reach.** The download page ships zero data links in its HTML;
the year picker and file table are built by
`https://www.nj.gov/education/spr/download/script/download.js`, which hardcodes
the base URL and filenames. A link-scraper gets nothing.

**CMS — Hospital Care Compare / Provider Data Catalog**
([topic page](https://data.cms.gov/provider-data/topics/hospitals)). The flat-file
zip `theme_hospitals_current.zip` holds 75 files: 72 CSVs plus
`HOSPITAL_Data_Dictionary.pdf` (105 pages), `Footnote_Crosswalk.csv`,
`Measure_Dates.csv`, `Data_Updates_April_2026.csv`, and a `manifest.json`.
From `Footnote_Crosswalk.csv`:

> `6,"Fewer than 100 patients completed the CAHPS survey. Use these scores with caution, as the number of surveys may be too low to reliably assess facility performance."`

From Appendix F of the dictionary: *"CMS retired data collection for the HCAHPS
Composites 3 (Responsiveness of Hospital Staff) and 7 (Care Transition)
beginning with the January 2026 release, these measures have been removed from
reporting."* **Honest-say caveat: yes** — suppression footnotes (blank is not
zero), reliability thresholds that forbid facility ranking, and a mid-series
measure retirement. **Discovery: the best of the twenty.** The dictionary is in
the zip, linked from the topic page, *and* declared in the DCAT catalog at
`https://data.cms.gov/provider-data/api/1/metastore/schemas/dataset/items` as
`"describedBy"` with `"describedByType": "application/pdf"`. Three independent
machine-readable routes.

**World Bank — World Development Indicators**
([catalog record](https://datacatalog.worldbank.org/search/dataset/0037712/World-Development-Indicators)).
`WDI_CSV.zip` contains six files, and only one of them is the data. The other
five are guidance shipped as tables: `WDISeries.csv` carries a *Limitations and
exceptions* column populated for **892 of 1,498 indicators**, alongside
*Statistical concept and methodology*, *Notes from original source*, and
*Development relevance*. `WDIfootnote.csv` carries **846,768 per-observation
footnotes** keyed on country, series, and year. `WDIcountry-series.csv` adds
7,939 country-specific source notes. From `WDISeries.csv`, indicator
`SL.UEM.TOTL.ZS`:

> "While the unemployment rate may be considered the most informative labour
> market indicator, reflecting the general performance of the labour market and
> the economy as a whole, it should not be interpreted as a measure of economic
> hardship or of well-being."

**Honest-say caveat: yes**, at indicator grain and at observation grain.
**Discovery: unavoidable if you unzip.** This is the closest thing in the
sample to SDMX-style attachable annotation, expressed as ordinary CSVs.

**US Census Bureau — TIGER/Line Shapefiles**
([landing page](https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-line-file.html)).
`tl_2024_10_place.zip` contains seven files, two of which are metadata:
`tl_2024_10_place.shp.iso.xml` (ISO 19115) and `.shp.ea.iso.xml` (ISO 19110
feature catalog). The disclaimer is in the first:

> "The boundary information in the TIGER/Line Shapefiles are for statistical
> data collection and tabulation purposes only; their depiction and designation
> for statistical purposes does not constitute a determination of
> jurisdictional authority or rights of ownership or entitlement and they are
> not legal land descriptions."

The XML also carries a precision trap the technical documentation's disclaimer
section does not: *"Coordinates in the TIGER/Line shapefiles have six implied
decimal places, but the positional accuracy of these coordinates is not as
great as the six decimal places suggest."* Worth noting for anyone quoting
this: the same disclaimer in
[`TGRSHP2025_TechDoc.pdf`](https://www2.census.gov/geo/pdfs/maps-data/data/tiger/tgrshp2025/TGRSHP2025_TechDoc.pdf)
§1.1 is worded differently — "is for" and a period where the XML has "are for"
and a semicolon. Two artifacts, one claim, two texts. **Honest-say caveat:
yes** (forecloses jurisdictional and positional claims). **Discovery: in every
zip** — but a fetcher that keeps only `.shp/.dbf/.prj` throws it away, and the
metadata files carry a *later* mtime than the data (2025-05-30 vs 2024-09-13):
the guidance was revised after the data shipped.

**CDC WONDER — Underlying Cause of Death**
([query page](https://wonder.cdc.gov/ucd-icd10-expanded.html)). Unique in the
sample: the caveats are appended to the result set itself, under a literal
`Caveats:` heading beside `Query Date:` and `Suggested Citation:`. From a live
query at `https://wonder.cdc.gov/controller/datarequest/D158`:

> "After the creation of the final 2023 dataset, North Carolina updated the
> cause of death information for over 900 death certificates to include a cause
> of death code indicating drug overdose… As a result, users should consider
> that the actual death count for drug overdose deaths for North Carolina in
> 2023 is over 4,400 deaths, with a crude rate of approximately 41.0 per
> 100,000 population… These deaths will not be updated on the final mortality
> datasets."

That is a publisher telling you the number in the file is wrong and supplying
the corrected figure in prose that will never appear in the data. The same
block flags a hard geography break: Connecticut's nine planning regions replace
eight legacy counties from 2022, and *"Populations estimates for the former
counties are not available for 2022 and later years."* The suppression rule
lives on the [documentation page](https://wonder.cdc.gov/wonder/help/ucd-expanded.html):
*"Statistics representing fewer than ten (one to nine) deaths or births are
suppressed."* **Honest-say caveat: yes**, and it is the only case in the sample
where the constraint is a *condition of access* — the click-through agreement
says *"Do not present or publish death counts of 9 or fewer or death rates
based on counts of nine or fewer."* **Discovery: inseparable from the result —
and unreachable.** WONDER returns 403 to non-browser clients; the caveats block
was captured only by driving a real browser session.

**BLS — Local Area Unemployment Statistics** ([program
page](https://www.bls.gov/lau/lauhome.htm), 403 to every automated client
tried). The public API returns a `footnotes` array on every observation. From
`https://api.bls.gov/publicAPI/v2/timeseries/data/` for series
`LASST060000000000003`:

> `{"code":"R","text":"Data were subject to revision on April 8, 2026."}`

The legend under the HTML series view at
`https://data.bls.gov/timeseries/LASST060000000000003` adds: *"X : Data
unavailable due to the 2025 lapse in appropriations."* **Honest-say caveat:
yes** — `X` means whole months of state labor-force data do not exist, so a
continuous trend line is an invention. **Discovery: split.** Footnotes arrive
unbidden in the JSON; the Handbook of Methods chapter that explains
benchmarking and model redesign is behind the same bot wall as the rest of
`bls.gov`, and no verbatim text could be retrieved from it. The API's richer
metadata is switched off outright: requesting `"catalog":true` returns
`"message":["The catalog has been disabled for this request."]`.

**NOAA NCEI — GHCN-Daily**
([directory](https://www.ncei.noaa.gov/pub/data/ghcn/daily/)). `readme.txt`
(28 KB) and `status.txt` (870 lines) sit in the same listable directory as
`ghcnd_all.tar.gz`. `status.txt` is a dated running errata log going back
years:

> "June 21, 2024
> Environment Canada's daily update feed was unexpectedly discontinued on April
> 28, 2024.  NOAA/NCEI is working to implement an alternative approach for
> updating Canadian station data."

`readme.txt` defines the quality and source flag vocabularies, including the
warning that source `S` values *"may differ significantly from 'true' daily
data, particularly for precipitation (i.e., use with caution)."* **Honest-say
caveat: yes** (a coverage gap in Canadian stations; a per-observation
reliability flag). **Discovery: one extra GET on a listable directory** — the
easiest non-trivial discovery in the sample.

---

## 2. Guidance in the portal's metadata

Four datasets keep the caveat in a single description string. This is the best
case for machine discovery and, with one exception, the shallowest content.

**City of Chicago — Crimes, 2001 to Present**
([`ijzp-q8t2`](https://data.cityofchicago.org/Public-Safety/Crimes-2001-to-Present/ijzp-q8t2)).
`metadata.attachments` is an empty array; there is no data dictionary, no
footnotes file, nothing but the description. Buried mid-paragraph in roughly
2,400 characters of mostly liability boilerplate, from
`https://data.cityofchicago.org/api/views/ijzp-q8t2.json`:

> "Therefore, the Chicago Police Department does not guarantee (either expressed
> or implied) the accuracy, completeness, timeliness, or correct sequencing of
> the information and the information should not be used for comparison
> purposes over time."

**Honest-say caveat: yes, and the strongest in the sample** — it forbids the
single operation most journalists perform on this file. The description also
notes that murders are one row per victim while everything else is one row per
incident, so naive row counts mix two units of analysis. **Discovery: trivial**
— one GET on the views JSON, and it is carried by the Discovery API too.

**LAPD — Crime Data from 2020 to Present**
([`2nrs-mtv8`](https://data.lacity.org/Public-Safety/Crime-Data-from-2020-to-Present/2nrs-mtv8)).
The landing URL still says "to Present" and still resolves, but redirects to a
record retitled *Crime Data from 2020 to 2024*. A banner delimited by literal
`******` markers opens the description:

> "As part of this transition, the legacy system is no longer active, and no new
> information will be entered. Consequently, the Crime Data from 2020 to Present
> dataset will no longer be updated. It will remain available on the portal for
> historical reference only."

**Honest-say caveat: yes — a hard stop.** The file is retired, the March 2024
UCR-to-NIBRS cutover makes either side non-comparable, and 2024 is truncated
mid-year. The description also admits *"This data is transcribed from original
crime reports that are typed on paper and therefore there may be some
inaccuracies within the data."* **Discovery: the notice is in the description,
but its pointers are broken for machines** — the two NIBRS successor datasets
appear as bare bracketed label text with no URLs, because the hyperlinks exist
only in rendered HTML. Three attached PDFs are all UCR-era, documenting the
standard the successor datasets no longer use.

**CDC — PLACES: Local Data for Better Health**
([`eav7-hnsx`](https://data.cdc.gov/500-Cities-Places/PLACES-Local-Data-for-Better-Health-Place-Data-2024/eav7-hnsx)).
The methodology caveat is in the Socrata description, not exiled to cdc.gov:

> "Because the small area model cannot detect effects due to local
> interventions, users are cautioned against using these estimates for program
> or policy evaluations."

**Honest-say caveat: yes** — the values are model-based small-area estimates
synthesized from BRFSS, ACS and Census, not local measurement, and the caveat
explicitly forecloses the most common intended use. (A further trap sits in the
release: 35 measures use 2023 BRFSS, five use 2022, so measures within one
release are not co-temporal.) **Discovery: one GET.** `metadata.attachments` is
empty; the linked measure-definitions page on cdc.gov returned 403 to every
automated client, so the portal copy is the only machine-reachable version.

**FTA — Transit Ridership, Fixed Route Bus** (National Transit Database, via
`https://data.transportation.gov/api/views/dwrv-9qyx.json`; `transit.dot.gov`
itself is 403 to all automated clients, so the NTD workbooks could not be
opened and no claim is made about whether they carry a notes tab):

> "Ridership estimates have been adjusted to account for changes in data
> collection over time. Starting in January 2012, data for Small System Waiver
> agencies that do not have a mode are reported under motor bus. Data reported
> under hybrid rail are reported under their classifications prior to January
> 2012."

**Honest-say caveat: yes** — a reporting-category change that shifts what
"motor bus" counts across a specific date. **Discovery: description field only**;
`metadata.attachments` is null, so a CSV or API consumer never sees it.

---

## 3. Guidance attached to the record, but off the catalog

**NYPD — Complaint Data Historic**
([`qgea-i56i`](https://data.cityofnewyork.us/Public-Safety/NYPD-Complaint-Data-Historic/qgea-i56i))
is the richest guidance in the sample and the hardest to reach by the
documented route. The description is two sentences and functions as a pointer:
*"For additional details, please see the attached data dictionary in the
'About' section."* The substance is in a five-page PDF of 24 numbered
footnotes, hung off the record as an attachment. Footnote 18:

> "These data represent criminal offenses according to New York State Penal Law
> definitions, not FBI Uniform Crime Report definitions, and are therefore not
> comparable to UCR reported crime."

Footnote 21 is a universe rule: *"Only valid complaints are included in this
release. Complaints deemed unfounded due to reporter error or misinformation
are excluded from the data set."* Footnote 22 removes most mala prohibita
offences — drugs, trespassing, theft of service, prostitution — so the file
cannot support drug-enforcement claims. Footnotes 5 and 6 reveal that rows are
keyed to *report* date, not occurrence date. Footnote 9 says the geocoding is
partly fictional (sex offences and un-geocodable offences are placed at the
precinct station house, Department of Correction offences at Riker's Island):
*"Any attempt to match the approximate location of the incident to an exact
address or link to other datasets is not recommended."* **Honest-say caveat:
yes, five times over** — and none of it is in the description.

**Discovery: this is the finding.** Attachments appear only in the
per-dataset views endpoint
(`https://data.cityofnewyork.us/api/views/qgea-i56i.json`, under
`metadata.attachments`), and retrieving one means hand-assembling
`/api/views/{id}/files/{assetId}?download=true&filename={filename}`. The string
"attachment" does not occur anywhere in the Socrata Discovery API response for
this dataset (`https://api.us.socrata.com/api/catalog/v1?ids=qgea-i56i`),
though the description — the one that says "see the attached data dictionary" —
does. There is no DCAT-US per-dataset endpoint and no `/files.json`. **The
federated catalog surface that aggregators consume advertises a data dictionary
it offers no path to.** The same negative was verified for LAPD.

---

## 4. Guidance on a page you have to go and find

The largest group. Six datasets keep the caveat that matters on a separate
page, a separate document, or a separate host.

**Census Bureau — ACS 5-year estimates**
([technical documentation](https://www.census.gov/programs-surveys/acs/technical-documentation.html)).
Guidance is extensive and completely detached from the data. Four separate HTML
surfaces: [comparison
guidance](https://www.census.gov/programs-surveys/acs/guidance/comparing-acs-data.html),
[errata notes](https://www.census.gov/programs-surveys/acs/technical-documentation/errata.html),
user notes, and table-and-geography changes, plus fourteen handbook PDFs. From
the comparison guidance:

> "Due to the impact of the COVID-19 pandemic, the Census Bureau changed the
> 2020 ACS release. Instead of providing the standard 1-year data products, the
> Census Bureau released experimental estimates from the 1-year data. Data users
> should not compare 2020 ACS 1-year experimental estimates with any other
> data."

The same page also states *"Do not compare overlapping datasets (example: do
not compare 2005-2009 ACS 5-year estimates to 2006-2010 ACS 5-year
estimates)."* Errata note 151 is more surgical: a data-processing error in the
2024 1-year employment tables propagates into the 2020-2024 5-year file, so
*"select estimates in these tables may not sum to the table subtotals."*
**Honest-say caveat: yes.** **Discovery: poor.** The FTP summary file splits
into `data/` and `documentation/`; `data/5YRData/` holds only `.dat` files, and
the `README.txt` in `documentation/` is 279 bytes containing a URL and a
feedback address. The API discovery document links to the developer page and
nothing else. Errata live at opaque numeric URLs (`errata/151.html`) findable
only by browsing.

**NCES — Common Core of Data**
([file listing](https://nces.ed.gov/ccd/files.asp)). The best-structured
guidance in the sample: the file listing renders three columns — Data File,
Documentation, Program File — with a companion file, release notes, and state
data notes per release, plus cross-year usage notes. From
[`CCD_Nonfiscal_DataFile_and_Usage_Notes.docx`](https://nces.ed.gov/ccd/doc/CCD_Nonfiscal_DataFile_and_Usage_Notes.docx):

> "Suppressed Data: LEA- and school-level data values that have been suppressed
> appear as null with DMS_FLAG set to "Suppressed."  Prior to SY 2016-17,
> suppressed values were set to "-9.""

From the [SY 2023-24 release
notes](https://nces.ed.gov/ccd/doc/SY_2023-24_Universe_1a_CCD_Nonfiscal_Release_Notes.docx):
*"two states, California and Oregon, do not routinely report prekindergarten
student membership data. These counts were imputed in many prior CCD releases
but were no longer imputed, starting with SY 2021–22."* **Honest-say caveat:
yes** — a sentinel-code regime change at SY 2016-17 that makes code written for
one era silently misread the other, plus named universe gaps (American Samoa
did not submit lunch or membership counts) that mean national totals are not
national. **Discovery: the docs sit beside the data links, but the zip is
bare** — `ccd_sch_029_2324_w_1a_073124.zip` contains exactly two members, a CSV
and a `.sas7bdat`. Nothing else. And the listing page is an Angular app
requiring three dropdown selections before any link renders.

**NHTSA — FARS**
([program page](https://www.nhtsa.gov/research-data/fatality-analysis-reporting-system-fars),
403 to automated clients; data at `https://static.nhtsa.gov/nhtsa/downloads/FARS/`).
The worst discovery story in the sample, attached to some of the most
consequential caveats. `FARS2023NationalCSV.zip` contains 34 files, all CSV,
all numeric codes, no manual, no readme, no codebook. Neither the FARS prefix
nor the year directory is listable, so a fetcher cannot walk the tree to find
the manual. The only pointer is a hand-maintained PDF of links at a path you
must already know
(`https://static.nhtsa.gov/nhtsa/downloads/FARS/Links%20for%20FARS%20Manuals.pdf`),
whose hyperlinks resolve to a third host with unstable numeric publication IDs
— `crashstats.nhtsa.dot.gov/Api/Public/ViewPublication/813706`, cited by
current search results, now 404s. From Appendix G of the *Analytical User's
Manual, 1975-2024* (`ViewPublication/813794`):

> "However, in compliance with Iowa's State Confidentiality Policy, death
> certificate data cannot be disclosed or re-released to the public. Therefore,
> starting in 2020, all data fields with death certificate-related data for Iowa
> will be filled with "Redacted" using values for the respective data elements
> as shown in the table below."

The same appendix admits a retroactive reclassification of large-truck crashes
that *"resulted in an understatement of large truck crashes through the years
and thus, an inaccurate assessment of the change in large truck crashes from
year to year"* — with *"Any issues existing in 2015 and earlier year files will
not be addressed due to a lack of source material needed for reconciliation."*
Appendix H records a universe change: *"For 2022 FARS is no longer collecting
motorized/motor assisted bicycles as motor vehicles."* **Honest-say caveat:
yes — suppression rule, universe change, retroactive correction, and a
two-version release cycle (annual report file vs. final file) where the same
crash year exists in two incompatible editions.** All of it invisible to
anyone who downloads the zip.

**FBI — Crime Data Explorer**
([downloads](https://cde.ucr.cjis.gov/LATEST/webapp/#/pages/downloads)).
Guidance exists in three places, none of them a download. Inline prose on the
downloads page, per collection:

> "Because the information in the tables of this publication is updated each
> year, the FBI cautions readers against making comparisons between the data in
> this publication and those in prior editions."

The FBI's long-standing position against ranking is a JavaScript modal on a
separate SPA route (`#/pages/help-center`): *"Data users should not rank locales
because there are many factors that cause the nature and type of crime to vary
from place to place."* Its text is not in the served HTML and not indexable.
The canonical PDF is stranded on the legacy host at
`https://ucr.fbi.gov/cautionagainstranking.pdf`, still the 2012 edition, with
no link from the CDE downloads page. The NIBRS trend break is buried in the
Help Center corpus: *"As 2021 was the first year NIBRS estimation data was
produced, the ability to compare estimated data across time will be limited."*
**Honest-say caveat: yes** — ranking prohibition, a 2021 series break, a
methodology divergence between CDE and the published tables, and open-ended
retroactive revision. **Discovery: only by browsing, with one escape hatch.**
Every download control is `href="#"` with a JS handler, so link-scraping yields
nothing; but the app fetches
`https://cde.ucr.cjis.gov/LATEST/webapp/assets/JSON/faq.json` (92 KB, the whole
Help Center as HTML strings) and
`assets/JSON/downloads/downloads.json` by plain GET.

**UK Department for Transport — Road Safety Data**
([data.gov.uk record](https://www.data.gov.uk/dataset/cb7ae6f0-4be6-4935-9277-47e5ce24a11f/road-safety-data)).
The CKAN `notes` field is a redirect notice and carries no caveats at all. The
guidance is four sibling resources under a "Supporting documents" heading, of
which two return 404 — including *Road Safety Data - Severity Adjustement
Giudance* (the publisher's own typos), which would have covered the single most
consequential caveat in the dataset. From the one document that does resolve,
[`Understanding-historical-road-safety-data.docx`](https://data.dft.gov.uk/road-accidents-safety-data/Understanding-historical-road-safety-data.docx):

> "Users should also consider whether sharp changes in trends are a result of
> genuine observed fluctuations or whether they are a result of different forces
> changing specifications from year to year."

It explains that STATS19 specifications were revised roughly every five years
and forces migrated at different times — *"In 2018, police forces were
independently reporting to the Department in 4 different specifications or
variants"* — so apparent jumps can be *"more observations being recorded, as
opposed to occurring."* Category codes changed meaning (car = 9 after 2005, 109
before); coordinate precision changed from 10 m to 1 m mid-series. **Honest-say
caveat: yes.** **Discovery: CKAN has the field and DfT left it empty.** All
five resources have `resource_type: null` and `description: null`, so the
"Supporting documents" grouping a human sees is not reconstructible from the
API — a fetcher must guess from the resource name string or the file extension.

**USDA ERS — Food Access Research Atlas**
([download page](https://www.ers.usda.gov/data-products/food-access-research-atlas/download-the-data)).
A split case. The zip does contain `SRAM Read Me.txt` beside the CSVs, but it is
navigational: it lists the six spreadsheets, gives the citation, and offers one
substantive line — *"Cells are intentionally left blank when data are
unavailable or not applicable."* Everything that constrains a claim is on the
separate [documentation page](https://www.ers.usda.gov/data-products/food-access-research-atlas/documentation):

> "FARA measures only one dimension of food access, geographic proximity, so
> these indicators do not capture other important factors such as food
> affordability, household resource constraints, store quality, and product
> availability."

The download page separately notes that the current SRAM release uses 2020
census tracts while the 2019 LRAM release uses 2010 tracts — a comparability
break between the two files a user is most likely to compare. **Honest-say
caveat: yes, but not in the artifact that travels.** The readme in the zip
would not stop anyone from making the wrong claim.

---

## 5. The opt-in case, and the empty case

**BTS — Reporting Carrier On-Time Performance**
([field picker](https://transtats.bts.gov/DL_SelectFields.aspx?gnoyr_VQ=FGJ&QO_fu146_anzr=b0-gvzr)).
The same table, two download paths, two different outcomes. The pre-zipped
monthly file
(`https://transtats.bts.gov/PREZIP/On_Time_Reporting_Carrier_On_Time_Performance_1987_present_2025_1.zip`)
always contains `readme.html` beside the CSV — a full record layout for ~110
columns. On the interactive path, the readme is a checkbox. From
`https://www.transtats.bts.gov/showHelp2.asp#_DOCUMENT`:

> "Select this box to generate a readme file together with the downloaded data.
> The readme file is in comma-delimited format and can be opened directly from
> the zip file in Excel."

That is the sharpest opt-in guidance in the sample: a fetcher on the primary UI
path gets no documentation unless it ticks two boxes it has no reason to know
exist. **Honest-say caveat: mixed.** The shipped readme is largely descriptive,
though the `Reporting_Airline` entry is a real correctness constraint — *"When
the same code has been used by multiple carriers, a numeric suffix is used for
earlier users, for example, PA, PA(1), PA(2). Use this field for analysis
across a range of years"* — and a user joining on `IATA_CODE_Reporting_Airline`
instead will silently merge distinct carriers. But the caveats that would most
change an honest claim, the Part 234 reporting threshold and the 2020 break,
are absent from every artifact that travels with the data and live only on
`bts.gov`, which is 403 to automated clients.

**GTFS — MBTA feed** (`https://cdn.mbta.com/MBTA_GTFS.zip`; spec at
[gtfs.org](https://gtfs.org/documentation/schedule/reference/)). The only clear
**no** in the sample. The zip contains 32 `.txt` files, all data — no readme,
no notes, no license. The single metadata file, `feed_info.txt`, is 247 bytes
of publisher name, language, validity window, version string and a contact
address. The spec provides no slot for prose guidance at all; the closest thing
is a pointer to a human, and even that is conditional. From the spec's file
table, `feed_info.txt` is *"Conditionally Required"* — required only if
`translations.txt` is provided, recommended otherwise. **Honest-say caveat:
none, except structurally** — `feed_end_date` (2026-09-05 in this feed) is the
one honesty-bearing field, and it carries no prose.

---

## The tally

| Publisher / dataset | Guidance | Where the caveat lives | In the download path? | Changes an honest claim |
|---|---|---|---|---|
| NJDOE School Performance Reports | yes | tab 1 of 63 in the workbook | yes (file URL is JS-only) | yes |
| CMS Hospital Care Compare | yes | PDF + CSVs inside the zip; DCAT `describedBy` | yes | yes |
| World Bank WDI | yes | four notes CSVs inside the zip | yes | yes |
| Census TIGER/Line | yes | ISO 19115 XML inside every zip | yes | yes |
| CDC WONDER | yes | `Caveats:` block appended to results | yes (403 to fetchers) | yes |
| BLS LAUS | partial | per-observation footnotes in API payload | yes (narrative docs 403) | yes |
| NOAA GHCN-Daily | yes | `readme.txt` + `status.txt`, same directory | yes | yes |
| Chicago Crimes 2001-present | partial | Socrata description field | metadata only | yes |
| LAPD Crime 2020-present | yes | Socrata description banner | metadata only | yes |
| CDC PLACES | yes | Socrata description field | metadata only | yes |
| FTA NTD bus ridership | partial | portal description field | metadata only | yes |
| NYPD Complaint Data Historic | yes | 24-footnote PDF attachment | views API only, not Discovery | yes |
| Census ACS 5-year | yes | four HTML sections + errata pages | no | yes |
| NCES Common Core of Data | yes | `.docx` beside the download link | no (zip is bare) | yes |
| NHTSA FARS | yes | manual on a third host, unstable ID | no | yes |
| FBI Crime Data Explorer | partial | JS modal + legacy-host PDF | no (JSON assets only) | yes |
| DfT Road Safety Data | partial | sibling `.docx` (2 of 4 are 404) | no | yes |
| USDA Food Access Research Atlas | partial | documentation HTML page | readme in zip is descriptive | yes (not in the artifact) |
| BTS On-Time Performance | partial | `readme.html`, opt-in on the UI path | pre-zipped yes, picker no | mixed |
| GTFS / MBTA feed | no | — | — | no |

---

## The four answers

**1. Roughly what share ships guidance that changes what a user may honestly
say?** Eighteen of twenty — 90%. Nineteen of twenty ship guidance of some kind;
GTFS is the only publisher with nothing, and it is the only one whose format
provides no slot for it. BTS is the one borderline case: it ships a readme, but
the readme is a record layout, and the comparability caveats live somewhere its
own data host does not reach. The caveats are not decorative. They are
comparability breaks (Chicago, ACS, FBI, DfT, NJDOE, NCES, CMS), suppression
rules (WONDER, CMS, NCES, FARS), universe changes (NYPD, NJDOE, FARS, WONDER),
and methodology changes (PLACES, LAPD, NTD). Several forbid, by name, the exact
operation a journalist opening the file would perform first.

**2. Which location is most common, and which is hardest to find?** Most
common is *a separate document or page on the publisher's site, not touching
the data* — eight of twenty (ACS, NCES, FARS, FBI, DfT, USDA, plus the
narrative layers of BLS and BTS). Second is inside the downloaded archive
(seven). Hardest for an automated fetcher is not one location but a pattern:
**guidance rendered by JavaScript or reachable only through an undocumented
endpoint.** The FBI's ranking statement is a modal whose text is not in the
served HTML. NJDOE's workbook URL exists only inside a `download.js` array.
NCES's documentation column renders only after three dropdown selections. And
the Socrata result is the sharpest: attachments — where NYPD keeps all 24 of
its footnotes — appear only in `/api/views/{id}.json` and are **absent from the
Socrata Discovery API**, the surface federated harvesters actually consume.
Verified negative for both NYPD and LAPD. The documented, federated metadata
path leads a machine to a description saying "see the attached data dictionary"
and then offers no attachment list.

**3. Discoverable from the download path alone?** For most, no. Seven of twenty
carry a claim-changing caveat in something that travels with the data — CMS,
WDI, TIGER, NJDOE, WONDER, BLS footnotes, GHCN. The other thirteen require
leaving the download and browsing the publisher's site. Every CSV endpoint
tested returned a bare header row: no comment preamble, no provenance rows, no
`Link:` header. Guidance and data are joined only by a landing page a human
reads. Two further failure modes compound this. **Guidance URLs rot faster than
data URLs**: `static.nhtsa.gov/.../downloadables/FARS/` is dead while
`/downloads/` lives, FARS publication 813706 now 404s, two of DfT's four
supporting documents are gone, and the LAPD attachment's `filename` and `name`
fields disagree so a URL built from the wrong one fails. And **the
infrastructure itself favours data over guidance**: `bts.gov`, `nhtsa.gov`,
`transit.dot.gov`, `bls.gov` and `wonder.cdc.gov` all return 403 to automated
clients while their data hosts serve fine.

**4. Does the hypothesis hold?** **It holds.** A cold reader's first genuinely
useful finding does come from the publisher's own words, and those words are
there to be found in nearly every case. Eighteen of twenty publishers have
already written down the thing that would otherwise be discovered the hard way
— often more precisely than a reader could reconstruct from the values (CDC
WONDER supplies the corrected North Carolina overdose count in prose; NCES
names the two states whose prekindergarten imputation stopped in a particular
year). Nothing in the data announces any of it.

For the hypothesis to fail, guidance would have to be either rare or empty:
most publishers shipping nothing, or shipping only descriptions of what the
columns contain. Neither is true. What the sample does show is a different
problem than the one the hypothesis was worried about. The risk is not that the
publisher's words do not exist — it is that **the words and the data are
connected only by a page a human reads**, and the connection degrades in
predictable ways: JavaScript rendering, undocumented endpoints, cross-host
manuals, unstable publication IDs, empty `resource_type` fields, bot walls in
front of the guidance but not the data, and typos in the filename of the one
document that mattered. A fetcher that follows only download URLs will miss the
caveat roughly two times in three — not because it was not written, but because
nothing in the download points at it.

---

*Twenty datasets sampled 2026-08 across federal statistical (ACS, BLS LAUS,
NCES CCD, CDC WONDER), municipal and state portals (NYC, Chicago, Los Angeles,
data.gov.uk), health (CMS, CDC PLACES), education (NJDOE), crime (FBI CDE),
geospatial (TIGER/Line), transport (BTS, FARS, NTD, GTFS), climate (GHCN-Daily),
food access (USDA ERS) and international (World Bank WDI). All quotations were
retrieved from the publisher's own page, file or API at the URL given.
`www.bls.gov`, `www.bts.gov`, `transit.dot.gov` and `cdc.gov/places` refused
automated clients; no text was reconstructed for those, and the gaps are noted
where they occur.*
