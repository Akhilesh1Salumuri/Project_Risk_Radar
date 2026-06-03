# Reference File Analysis

Generated from the four Excel reference files in `data` to support multi-format ingestion testing and project-risk knowledge tuning.

## Parser Results

| File | Parsed Records | Main Project Interpretation |
|---|---:|---|
| `EBS Development Project Status_2022.xlsx` | 226 | Mixed EBS development portfolio of projects, CRs, problem tickets, WIP, sprint tasks, and RMS hypercare items |
| `In Store Ecomm Rollout Plan New - V2.0 (1).xlsx` | 107 | One rollout programme split by market/brand workstreams |
| `Mpos Checklist & Pilot Plan.xlsx` | 236 | One MPOS pilot/rollout programme with checklist, pilot plans, market rollout plans, terminal/store data |
| `Roadmap - As is and To be - MDM Process Mapping - v3.xlsx` | 243 | Two related MDM process mapping streams: Product MDM and Location MDM |

## EBS Development Project Status_2022.xlsx

Project context: This is not one project. It is a mixed EBS development and support portfolio containing problem tickets, projects, CRs, WIP schedules, ongoing development items, sprint-plan tasks, RMS hypercare issues, and summary pivots.

People and teams identified:
- People/owners: Siva, Raghu, Mohammed, Bala, Vishnu, Anthony, Shabuddin, Venkat, Ramesh L, Hema, Chowri, Archana.
- Teams/roles: BA, Developer, BA / Developer, FIN App, Ops team, Fin App team, Oracle Support, ES RMS, ES Finance, EBS Ops, RMS Ops, Business Users, RPA Team.

Dates and task meaning:
- ETA cells are used as delivery target dates for individual problem tickets or change/project items.
- Status notes include event dates such as UAT sign-off, production migration, deployment completion, user confirmation, RCA review, and prioritization checks.
- Summary sheets dated `30 Nov 2022`, `08 Jan 2023`, and `06 Feb 2023` are portfolio reporting snapshots.
- Sprint-plan dates such as `6-FEB-23` identify planned SIT/UAT timing for specific development tasks.

Useful risk-learning patterns:
- UAT sign-off pending, awaiting business confirmation, user feedback, RCA incomplete, prioritization/resource allocation, incorrect balances, data fixes, reconciliation issues, Oracle escalation.

## In Store Ecomm Rollout Plan New - V2.0 (1).xlsx

Project context: This is one programme, `InStore Ecomm Rollout`, split across market/brand workstreams: KW H&M, UAE BBW, QTR H&M, KSA H&M, Drupal ETA, MDM ETA, notes, and questions. It should be treated as a mixed-workstream rollout file, not unrelated projects.

People and teams identified:
- People/owners: Akhilesh, John, Ginger, Mark, Mark Smith, Rabih Hassan, Amjad Al Shaiah, VijayKumar Reddy, Sanam Parkar, Pradeep, Mohamed Kashif, Joshua, Bince, Razeem, Store Associates.
- Teams/roles: Brand Team, Change Team, Project Team, Drupal, Magento, O365 Team, Regional IT, Regional IT Team, Brand Training Team, Store Manager, Champions, VMO, Product Team, Rollout, BAU, CAC, RIT, Data, Brand Ops.

Dates and task meaning:
- Project start date is `2022-07-08`.
- Weekly timeline headers run from `2022-07-08` through early 2023 and represent planning periods.
- Row-level `Start` and `End` dates represent activity windows for form filling, training, Drupal configuration, MDM enrollment, procurement, distribution, and go-live support.
- `Drupal ETA` and `MDM ETA` sheets include rollout/configuration ETA dates, procurement dates, and good-to-have dates by market/brand.
- Notes mention DDR dates around `21 August` and `21 September`.

Useful risk-learning patterns:
- Not Started / In Progress rollout tasks, Drupal configuration, user creation, MDM enrollment, procurement, dependency on brand/store information, questions requiring decision ownership.

## Mpos Checklist & Pilot Plan.xlsx

Project context: This is one `MPOS Pilot Rollout` programme with multiple views: checklist, pilot plans, KW pilot/rollout schedules, UAE terminal information, and KW rollout store data.

People and teams identified:
- People/owners: Sahaya Johney, Naveen, Tony, Ginger, Ruel, Faji, Abdul Sharif, Laura, Mahesh, Rajesh Kumar, Sheena, Syed, Azhar, Aben, Vaheed, Akhilesh, Johney, Jijin, Joseph, Razeem.
- Teams/roles: O365, KW RIT, RIT, Rollout Team, Product Team, Delivery Team, Store Team, Brand Ops, Change, Central Ops, Supplier, Payment, KNET, CPD, UAE VMO Team, Finance, NetOps, Bank, ARES Ops/RIT, IAML2.

Dates and task meaning:
- Checklist note says supplier finalization on `26 Jun`; this is a procurement/supplier dependency date.
- Pilot plan starts on `2023-07-04`; row-level dates define task windows for device registration, MDM profiling, configuration, training, handover, payment terminal readiness, and SOP tasks.
- KW rollout starts on `2023-07-25`; dates through late August/early September represent rollout task windows.
- KW pilot and MPOS pilot sheets start on `2023-10-04`; dates into November represent pilot/brand scaling windows.
- Store and terminal sheets contain rollout scope/reference data, not task due dates.

Useful risk-learning patterns:
- To be confirmed, process to be decided, supplier finalization, device availability, payment terminal availability, charging capacity, printer availability, Ops/SM confirmation, Not Started rollout tasks.

## Roadmap - As is and To be - MDM Process Mapping - v3.xlsx

Project context: This workbook contains related process mapping streams rather than one flat project: `Product MDM Process Mapping` and `Location MDM Process Mapping`, plus deliverables, RACI, stakeholders, and process-vs-stakeholder coverage.

People and teams identified:
- Workstream owners/initials: AT, OJ, NH, DIT, JS.
- RACI names: Aya, Owen, Natasha, Jan.
- Stakeholders: Najeebudheen C.E, Mohamad Kalche, Jisha Sara, Ravi Teja Reddy Kareddy, Liane Dsouza, Deepti / Taiyeb, Raghdaa Al Sebai, Arun Alex Philip Palavilayil, Pierre Faure, Pratyusha Singirgari, Bill O'Shea, Joanne Brett, Olena Lemeshko, Sunish Nair, Muthukrishnan Jayaraman, Anwar Al Qaisi, Claire Robinson, Chris Dalrymple, Michelle Pocock.
- Teams/roles: Business / Brand Division, DG & Process Team, IT Business Partner, Change Management Team, IT, Food, Beverage & Retail Lobby, QA, Online Trading, Brand Support, Supply Chain, Ops Services, FMC, Simphony, My Micros, Nutritics.

Dates and task meaning:
- Product roadmap uses weekly buckets from May through November.
- Location roadmap uses weekly buckets from May through September.
- `29/30 June` is an Eid scheduling consideration.
- `post August` is a dependency point for iteration 1 prototype MDM solution.
- `mid October` is an assumption for iteration 2 readiness for business rollout.

Useful risk-learning patterns:
- Stakeholder identification, workshop planning, as-is discovery, sign-off, dependency on MDM prototype, assumed readiness dates, RACI ownership, data/process mapping, manual upload process ownership.
