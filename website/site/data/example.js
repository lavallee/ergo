window.__ERGO_PAGE__ = {
  "path": "examples/spr.md",
  "dataset": {
    "ergo": "0.5",
    "slug": "spr",
    "title": "NJ School Performance Reports",
    "publisher": "NJ Dept. of Education, Office of Performance Reports",
    "subject": "https://www.nj.gov/education/spr/",
    "contribute": "https://github.com/lavallee/ergo/issues",
    "source_urls": [
      "https://www.nj.gov/education/spr/"
    ],
    "pitfall": "NJ publishes two 4-year graduation rates; only the State calculation has a multi-year trend — plotting the Federal rate as a trend (it has one point) is the classic misread.",
    "status": "live",
    "version": "2024-25 edition",
    "confidence": "A",
    "updated": "2026-07-31",
    "implementation": "https://github.com/lavallee/njschooldata",
    "unknowns": [
      "Pre-2015-16 editions have not been examined; the format eras before that are unknown to us.",
      "We do not track which NJSLA cut scores changed between editions."
    ],
    "coverage": {
      "years": "2015-16 → 2024-25 (trend tabs post-COVID only)",
      "grain": "school year × entity × student group",
      "entities": "every NJ public school, district, and the state"
    },
    "missingness": {
      "zero_is_missing": false,
      "source_tokens": [
        "*",
        "N",
        "Fewer than 10 valid scores"
      ]
    },
    "access": {
      "keys": [
        "county_code",
        "district_code",
        "school_code",
        "school_year"
      ],
      "raw": "data/raw/spr/",
      "builders": [
        "tools/build_spr_db.py"
      ],
      "feeds": [
        "grad_rate",
        "assessment",
        "assessment_grade",
        "absenteeism",
        "growth"
      ]
    },
    "acquisition": {
      "access": "public",
      "terms": "Public NJ education records; preserve NJDOE's own terms on redistribution.",
      "credentials": "none",
      "format": "One XLSX workbook per year, ~80 tabs; a companion layout workbook is the data dictionary.",
      "method": "Published index page, then direct per-year file URLs.",
      "cadence": "annual",
      "lag": "Published the autumn after the school year it describes.",
      "verification": "Watch the index for a new workbook and record the first date seen.",
      "size": "~330 MB at school level for the current year."
    }
  },
  "issues": [
    {
      "id": "url-host-split",
      "title": "Files live under /education/sprreports/, not the /education/spr/ landing path",
      "effect": "breaks",
      "type": "availability",
      "status": "mitigated",
      "discovered": "2026-06",
      "handled_by": [
        "tools/build_spr_db.py"
      ],
      "detection": "404s when constructing file URLs from the landing-page path",
      "scope": {
        "all": true
      },
      "_line": 89
    },
    {
      "id": "layout-types-lie",
      "title": "Code columns typed 'Numeric' in the layout are zero-padded TEXT in the data",
      "effect": "corrupts",
      "type": "format",
      "status": "mitigated",
      "discovered": "2026-06",
      "handled_by": [
        "tools/build_spr_db.py"
      ],
      "detection": "CountyCode='13', DistrictCode='4900' — string cells with leading zeros preserved",
      "misuse": "Coercing codes to integers strips leading zeros and silently breaks the warehouse join.",
      "scope": {
        "columns": [
          "CountyCode",
          "DistrictCode",
          "SchoolCode"
        ],
        "all": true
      },
      "_line": 110
    },
    {
      "id": "rate-prose-suppression",
      "title": "Rate cells carry % signs, prose suppression sentences, and >90%/<10% privacy caps",
      "effect": "breaks",
      "type": "suppression",
      "status": "mitigated",
      "core": true,
      "discovered": "2026-06",
      "handled_by": [
        "tools/build_spr_db.py#rate"
      ],
      "detection": "value fails float() after stripping a trailing % — includes '>90%', '<10%', and sentences like 'Fewer than 10 students were in the graduation cohort.'",
      "misuse": "Treating suppression NULLs as zero. Capped extremes also go NULL — harmless for All Students, a real loss for small subgroups.",
      "instead": "Leave suppressed values NULL, exclude them from denominators, and say so in captions for small subgroups.",
      "scope": {
        "tables": [
          "grad_rate",
          "assessment",
          "assessment_grade",
          "absenteeism"
        ],
        "columns": [
          "*Rate*",
          "*Percent*"
        ],
        "years": "all"
      },
      "detect": {
        "regex": [
          "^(>|<)\\\\d+(\\\\.\\\\d+)?%$",
          "Fewer than 10 (students|valid scores)"
        ],
        "semantic": [
          "a rate column parses as numeric for some rows and prose for others"
        ]
      },
      "_line": 133
    },
    {
      "id": "grad-state-vs-federal",
      "title": "State and Federal 4-yr graduation rates coexist; only State is populated across years",
      "effect": "misleads",
      "type": "measurement",
      "status": "mitigated",
      "discovered": "2026-06",
      "handled_by": [
        "tools/build_spr_db.py"
      ],
      "detection": "4YrGraduationRateState_District non-empty in 27,115 of 27,201 trend rows; Federal in only 5,423 (≈ one year)",
      "misuse": "Drawing the Federal rate as a trend line (it has one point), or comparing a State figure against another state's federal ACGR — NJ's State calc runs higher (SOMSD 2024-25: State 93.2% vs Federal 89.4%).",
      "instead": "Plot the State rate as the trend; headline the latest-year Federal ACGR beside it and caption the difference.",
      "scope": {
        "tables": [
          "grad_rate"
        ],
        "columns": [
          "4YrGraduationRate*",
          "5YrGraduationRate*"
        ],
        "years": "all"
      },
      "_line": 163
    },
    {
      "id": "grade-mix-context",
      "title": "District/state context blends all tested grades; a school's value covers only its own",
      "effect": "context",
      "type": "definitional",
      "status": "open",
      "discovered": "2026-06",
      "misuse": "Reading a high school's math proficiency sitting below its district as a deficit — the district figure blends grades 3–8 with HS course tests over different populations.",
      "scope": {
        "tables": [
          "assessment"
        ],
        "all": true
      },
      "_line": 187
    }
  ],
  "practices": [
    {
      "id": "headline-proficiency-as-published",
      "title": "Use NJDOE's published school-wide proficiency; do not rebuild it from grade/test rows",
      "question": "What share of this school's students met or exceeded expectations?",
      "authority": "publisher",
      "rule": "Read the school-wide MetExceed value NJDOE publishes at the school grain.",
      "naive": "Averaging or summing the per-grade, per-test rows in assessment_grade up to a school figure.",
      "because": "Suppressed cells drop out of a home-grown aggregate silently, and grade/course mix differs by school — one capped Algebra I cohort once inflated a school's rebuilt figure well above its published one.",
      "addresses": [
        "rate-prose-suppression",
        "grade-mix-context"
      ],
      "implemented_by": [
        "tools/build_spr_db.py#headline"
      ],
      "residual": "We inherit NJDOE's own inclusions and exclusions, which are not fully documented; our figure matches the published one and is no more transparent than it.",
      "_line": 209
    },
    {
      "id": "grad-calcs-stay-separate",
      "title": "Report the State and Federal graduation rates as distinct measures, never combined",
      "question": "What is this district's four-year graduation rate?",
      "authority": "project",
      "rule": [
        "Use the State calculation for any multi-year trend — it is the only one populated across years.",
        "Report a Federal (ACGR) figure only as a single labelled year.",
        "Never average, splice, or plot the two in one series."
      ],
      "naive": "Plotting whichever rate is present per year, producing one line that silently switches definitions.",
      "because": "The two use different cohort rules; a spliced series shows a step change that is an artifact of the definition, not of any school's performance.",
      "addresses": [
        "grad-state-vs-federal"
      ],
      "contested": true,
      "because_not": "We considered publishing only the Federal rate for cross-state comparability and rejected it: with one populated year it answers almost no question a reader actually asks about NJ.",
      "_line": 229
    }
  ],
  "references": [
    {
      "id": "njschooldata",
      "kind": "implementation",
      "url": "https://github.com/almartin82/njschooldata",
      "observed": "2026-07-30",
      "commit": "9c34401276d3d7fb45bdbd62ef927db6e252b933",
      "covers": "R fetchers for NJ DOE series; fetch_spr() builds SPR database URLs for end_year 2017-2025 at school or district level.",
      "maintenance": "active",
      "_line": 253
    }
  ],
  "quotes": [
    {
      "text": "The School Performance Reports reflect the New Jersey Department of Education's (NJDOE) commitment to providing parents, students, and school communities with a large variety of information about each school, each district, and the state overall.",
      "source": "https://www.nj.gov/education/spr/",
      "retrieved": "2026-07-30",
      "supports": [
        "headline-proficiency-as-published"
      ],
      "note": "A reader-facing publication, which is why suppression arrives as prose in a cell and why the headline figures are NJDOE's to compute, not ours.",
      "_line": 68
    }
  ],
  "validations": [
    {
      "date": "2026-06-14",
      "method": "confirmed from real data — 2024-25 District/State file",
      "result": "codes are zero-padded TEXT; All-Students label is 'All Students'; suppression is prose sentences; SchoolYear format matches warehouse",
      "_line": 270
    }
  ],
  "changes": [
    {
      "date": "2026-07-10",
      "note": "Page created in ergo format; 5 issues registered from the 2024-25 acquisition notes.",
      "_line": 285
    },
    {
      "date": "2026-07-30",
      "note": "Quoted NJDOE's own statement of what the reports are for, under What it is.",
      "_line": 291
    },
    {
      "date": "2026-07-31",
      "note": "Recorded almartin82/njschooldata as an existing R implementation of these workbooks.",
      "_line": 297
    },
    {
      "date": "2026-07-31",
      "note": "Added the acquisition table: access level, terms, cadence, lag, and how to tell a new release landed.",
      "_line": 303
    }
  ],
  "prose": {
    "url-host-split": "The landing page is a JS app whose `download.js` builds the real links:\n`https://www.nj.gov/education/sprreports/download/DataFiles/<YEAR>/<file>`\nwith hyphenated years (`2024-2025`). Easy to fetch the wrong path.",
    "layout-types-lie": "Confirmed against the 2024-25 District/State file: the data cells match the\nwarehouse's TEXT keys verbatim, so the *correct* behavior is to trust the\ndata over the data dictionary.",
    "rate-prose-suppression": "Parse rule: a value is a number iff it parses after stripping a trailing\n`%`; everything else → NULL. Four distinct suppression sentences observed in\nthe 2024-25 files, plus the two extreme caps.",
    "grad-state-vs-federal": "The trajectory uses the State calculation; the latest-year Federal ACGR is\nheadlined where present, with the difference noted in the caption.",
    "grade-mix-context": "Real, not a bug: comparisons across aggregation levels compare different\ngrade mixes. Per-grade views (`assessment_grade`) are the honest grain.",
    "headline-proficiency-as-published": "The reader-facing number on NJDOE's own report card is the published one.\nAny figure we compute that disagrees with it will be read as an error in our\nwork, and usually is.",
    "grad-calcs-stay-separate": "Cross-state comparison is the one job the Federal rate does better, and it\nis worth saying out loud that another newsroom covering multiple states\nmight reasonably invert this call.",
    "njschooldata": "Recorded because it is the shortest route to the same workbooks for anyone\nworking in R, not as an endorsement — no `caveat` here means it has not been\njudged, only observed."
  },
  "check": "1 page(s), 5 issue(s), 2 practice(s): 0 error(s), 0 warning(s)",
  "lede": "Worked example of an ergo data page, condensed from the real page in\n[njschooldata](https://github.com/lavallee/njschooldata). New Jersey's\nofficial annual \"report card\" for every public school and district —\nassessments, graduation, absenteeism, growth — and the authoritative source\nfor academic-outcome reporting."
};
