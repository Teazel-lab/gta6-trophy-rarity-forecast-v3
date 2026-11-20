# R2 — Week-one trophy curves (story launches)

Priors for Exophase earn rates from **day 2.5 to day 7.0** of GTA VI: 60 h to 168 h after 2026-11-19T00:00Z. That span is the final case (checkpoint 2026-11-21T11:30Z, target 2026-11-26T00:00Z, 108.5 h). `Δx = ln(169) − ln(61) = 1.019`, so a logit change `Δ` is a house-curve slope of `Δ / 1.019` per `ln(1+hours)`.

Rates below are whoever each source counts. Exophase is **not** PSN-wide. Judgment rows are marked as such. Day-2 vs day-7 snapshots for the same trophy are rare; most public numbers are one date.

## 1. What was actually measured

**Marvel’s Spider-Man 2** (PS5, 20 Oct 2023, story ~15–20 h, platinum ~25–35 h). PSN-wide, via Push Square / JorRaptor on 25 Oct (“not even one week”): story **24.5–25%**, platinum **6.3%**. By 27 Oct 09:35, a PS5 trophy roundup: story **29.9%**, platinum **8.6%**.

- Story logit −1.099 → −0.852 (**+0.25**), ratio 1.20, over ~2 days late in week 1.
- Platinum logit −2.70 → −2.36 (**+0.34**), ratio 1.37.
- Mature (2026): Exophase story 75.3%, platinum 50.7% (200,595 tracked). Same page on PSNProfiles: story 81.5% site / **53.6% Sony**; platinum 65.1% site / **15.7% Sony**.

**God of War Ragnarök** (9 Nov 2022, story ~20 h, platinum ~40–50 h on easy). About **15–16 days** out, not day 7. Push Square 24 Nov: story **24.8%**, platinum **3.9%**. TrueTrophies 25 Nov: story trophy **26.8%**, epilogue **17.9%** (about one in three finishers had not seen it), platinum **4.4%**. A 20 h finale was still only ~1 in 4 after two weeks, on the global PSN base.

**Elden Ring** (25 Feb 2022). By ~18–19 days (15 Mar), Steam: Margit **70.7%**, Roundtable Hold **78.1%**, Godrick **61.3%**, an ending **~17%**. PlayStation the same day: Margit **68%**, Godrick **57.6%** (Eurogamer). A separate note the same day put PlayStation *ending* trophies near **5%** — that is one ending each, not “any ending”; do not average it with Steam’s 17%. Gamepressure’s 7 Mar → 14 Mar table (already week 2, rates high): Steam Margit 66.2→70.3 (**+0.19 logit**), Godrick 55.9→60.8 (**+0.20**); their PSN Godrick column 62.2→71.2 (**+0.41**). Once a boss is common, a further week is only a few points.

**Red Dead Redemption 2** (26 Oct 2018, story ~50–60 h, platinum 200 h+). A PSN paste dated 13 Dec 2018 (~48 days): Ch1 **86.3%**, Ch2 **58.0%**, Ch3 **42.7%**, Ch4 **32.8%**, Ch5 **30.7%**, Ch6 **23.4%**, epilogue **18.7%**. Press in Jan 2019 put full-story completion near **22%**. Mature Exophase (Nov 2026, ~517k tracked): Ch1 **82.8%**, Ch2 **60.8%**, Ch6-ending **44.2%**, epilogue **40.6%**, 100% **4.0%**, platinum **2.7%**. PSN Trophy Leaders’ Sony column is lower and the gap widens as the trophy gets rarer: Ch1 Sony **64.9%** vs site **84%**, Ch2 **42.4%** vs **63%**, platinum Sony **0.1%** vs site **~4%**. Ch1 being *higher* at day 48 (86%) than Sony’s long-run 65% is dilution by later buyers, not players losing the trophy.

**Hogwarts Legacy** (7–10 Feb 2023, story ~35–45 h, platinum ~60–80 h). No clean day-7 cut found. By late March 2023, one multi-platform roundup had the finale near **30–41%** depending on platform (PS5 cited around 35–41%). Mature tracker rates sit far above Sony on the platinum (a PS4 sample on PSN Trophy Leaders: site **17%** vs Sony **~1%**).

**Cyberpunk 2077** (10 Dec 2020). First PSNProfiles story unlocks **7 Dec** (review/early copies). No trustworthy global % for week 1. Mature “finish the story” is roughly **30%** on several platforms. Useful only as: a ~25 h campaign does not hit a third of all players quickly, and the first finishers are a tiny named tail.

**Starfield** (premium 1 Sep 2023, wide 6 Sep). TrueAchievements: **909** players had the final main-quest achievement *before* the wide launch, after about a week of early access. Absolute counts, not a rate. The tail is real; it is hundreds of people against millions of owners.

**GTA V PS4** (18 Nov 2014, story ~30 h). First tracked unlock of the final mission on PlayStationTrophies: **19 Nov 2014**. A 30 h GTA can be finished inside a day by the extreme tail. Mature PSNProfiles: that trophy ~30% of site owners, platinum ~2%.

No archived Exophase day-2 and day-7 pair for these games turned up. The shape below is from these cuts plus the two-force identity, not from a fitted historical panel.

## 2. Dilution vs progression

`r = E / N`. Over a gap, if new tracked players arrive with the trophy still locked and a fraction `f` of the *old* cohort earns it:

`r' = (r + f) / (1 + g)`, `g = N_new / N_old`.

Logit falls by about `ln(1+g)` when nobody new earns it. `g = 1` (tracked population doubles) is **−0.69 logit** of pure dilution.

**Own reads, 20 Nov 2026, ~11:10Z → ~16:00Z** (N 36,080 → 44,161, `g = 0.22` in ~5 h): Chapter 1 **7.99% → 11.98%** (earners ~2,880 → ~5,290, **+0.45 logit**, ratio 1.50). Chapter 2 **0.90% → 1.71%** (**+0.65 logit**, ratio 1.90). Implied `f` on the old cohort: **6.7 pp** for Chapter 1, **1.2 pp** for Chapter 2. Progression beat a 22% bigger denominator. Local slope vs `ln(1+h)` is ~**3.5** for Chapter 1 — an in-session burst, not a week-long slope. Freezing it through day 7 sends a 12% trophy toward ~90%. That is an upper tail.

Which force wins:

- **Early story (a few hours).** Progression wins in week 1 on a front-loaded launch. New players also clear the gate inside the same week, so dilution is temporary. The rate climbs and then flattens (Spider-Man story +0.25 logit in the *second half* of week 1; Elden Ring’s first boss only +0.2 logit per week once it is already ~65%). Ceiling on a hunter site can sit at 70–90% even years later; PSN-wide ceilings are lower (RDR2 Ch1 ~65% Sony vs ~83% Exophase).
- **Mid story (about 15–35 h).** Progression still wins on Exophase in week 1, because the tracked set is the people playing. The weekend does most of the work. Global PSN moves slower: RDR2 Ch2 was still 58% at day 48.
- **Late story / credits (45–70 h).** A thin tail. By day 7 only no-lifers and people who started in NZ/AU on 18 Nov. Dilution can match progression. Expect a rise from a near-zero base, not a march toward the two-week “25% finished” headlines (those were 15–20 h games, PSN-wide, at day 14+).
- **Platinum and 100%.** Near 0 all week, on every comp above. Ragnarök’s easy platinum was 4% at day 15. RDR2’s is still ~3% on Exophase after years. Wall-clock makes GTA VI’s ~200 h platinum almost unreachable by 26 Nov (see §3). Dilution does not matter; the level is a floor.
- **Side, collectible, stunt, money counters.** No story gate. Small “try it once” tasks track early story. Large counters (250 stunts, 100 vehicles, full card sets, $250k) track the platinum: they move only with many sessions and stay rare all week. Optional stranger finales sit between mid story and late story, with a lower ceiling because many players skip them (Ragnarök: a third of story finishers missed the epilogue at day 16).

**Exophase vs PSN-wide.** Sony’s % is every account that holds the list. Exophase’s % is accounts it tracks — people who linked a profile. PSNProfiles is a still tighter hunter set. Forum note from Exophase (2019): linked users are trophy hunters, and the site’s rarity is its own users. psn.gg states the same split. Empirically Exophase sits **between Sony and PSNProfiles, closer to the hunter site** (Spider-Man 2 platinum 16% Sony / 51% Exophase / 65% PSNProfiles). The hunter/global odds ratio is near 1.2–1.5 for very common trophies and enormous for the platinum (RDR2 ~3% vs 0.1%). Week-1 Exophase rates should run **hotter** than a PSN headline for the same trophy, and the gap should be widest on late and completion trophies. Exophase’s *denominator* still grows fast at launch (638 pre-release → 3,868 at the first refresh → 36k by 20 Nov 11:10Z → 44k by ~16:00Z). That is linking lag, not sales. A further **2–4×** by day 7 is a reasonable planning range (`g ≈ 1–3` from the day-2 base, **−0.7 to −1.4 logit** if earners froze). It is a judgment, not a measured law.

## 3. GTA VI facts that set the clock

Release is **midnight local, 19 Nov 2026**, rolling by country. New Zealand: **18 Nov 11:00Z**. UK: **19 Nov 00:00Z** (the contest epoch). US East: **19 Nov 05:00Z**. US store listing was one national midnight (Eastern), so the West got it the evening of 18 Nov local. From those unlocks to 26 Nov 00:00Z the wall clock is about **181 h (NZ), 168 h (UK), 163 h (US East)**. A 200 h completion does not fit in the window except a sleepless NZ outlier, and even that is short of 200.

**19 Nov 2026 is a Thursday.** The checkpoint (Sat 21 Nov 11:30Z) is **06:30 US Eastern Saturday** — the US weekend binge is still ahead of the last read the model will see. The target (Thu 26 Nov 00:00Z) is Wednesday evening in the US. The horizon contains **Sat–Sun plus Mon–Tue**, the days a Thursday launch actually gets played. A log-time line fit on Friday’s refreshes does not contain that step.

Length, from launch reviews and guides (they disagree on the margin):

- Story-only about **50–60 h**; rushed press runs **42–50 h** (Pure Xbox 42 h, HowLongToBeat’s first main-story submission 42 h). With side content **65–115 h** (Eurogamer ~65, IGN 70 and 115). Rockstar’s Rob Nelson: **~80 h** including some optional goals (NYT, via several 27 Aug and Nov write-ups).
- **Five chapters, ~91–93 main missions.** Counts that recur: Ch1 **22**, Ch2 **7–13** (Output Lag says 7; several guides say 11 or 13), Ch3 **24–26**, Ch4 **25**, Ch5 **7–8**. VGC’s Chapter 1 guide: **~6–7 h** rushed, **~10 h** with side content. Output Lag also puts Chapter 1 near 10 h.
- **Trophy names are the contract, not guide chapter titles.** In the case file, Paradise Lost is *Complete Chapter 1*, and the next bronze is Chapter 2. Some guides hang “Paradise Lost” on their Chapter 2. Mission counts are still the best length prior.
- **100% / platinum ~150–300 h**, center **~200 h** (Insider Gaming, PowerPyx, Push Square). Checklist is large (stunts, races, animals, vehicles, challenges). Output Lag on 20 Nov: **no confirmed 100% save yet**. No source found here of a public player platinum in the first ~36 h. Reviewers finished the *story* before street date; that does not put the platinum on the board.
- Sales are front-loaded. Sensor Tower, reported by BBC and GamesIndustry on 20 Nov: **~24.5–24.6 M** copies through launch day including pre-orders, **~75% PS5 (~18.4 M)**, about **$2.36 B**. A second tracker (AppGazers) printed a higher ~30 M by 20 Nov; treat it as a different estimate. Pre-orders were the bulk, so *buyer* dilution in week 1 is milder than a game that sells steadily into Christmas. Exophase’s ~44k on 20 Nov is on the order of **0.2%** of PS5 copies.

Play-time vs calendar, judgment: a typical linked player might have ~10–20 h by Saturday morning and ~25–45 h by Wednesday night if they play the weekend hard. That clears Chapter 1 for a large minority, Chapter 2 for a smaller one, Chapter 3 only for a heavy weekend, and Chapters 4–5 only for the tail. It does not clear 100%.

## 4. Priors: rate `r` at 60 h → 168 h

`Δ` is `logit(r_day7) − logit(r_day2.5)`, in logit units, after clamping thoughts to the scoring range 0.01–99.99. The **5–95%** column is a judgment interval for that change, meant to be wide. It is not a standard error from a regression. Ratio column applies while `r` is small enough that `1−r ≈ 1`; near a ceiling, use the logit and cap the level.

| Class | Hours | Typical `r` at 60 h | Center `Δ` | 5–95% `Δ` | Ratio if still small | Slope `/ln(1+h)` |
| --- | --- | --- | --- | --- | --- | --- |
| Early gate (Ch1, Gone Fishing, first activities) | 2–10 | 8–25% | **+1.0** | **+0.2 to +2.2** | 2–3.5×, ceiling ~45–70% on Exophase | **~1.0** (0.2–2.2) |
| Mid story (Ch2, Ch3, a stranger finale) | 15–35 | 0.5–8% | **+1.3** | **+0.2 to +2.8** | 2.5–6× | **~1.3** |
| Late story (Ch4, Ch5, final mission) | 45–70 | 0.05–1% | **+1.4** | **−0.2 to +3.2** | 3–8×, day-7 level mostly 1–8% | **~1.4**, residual huge |
| Platinum, 100%, huge counters (250 stunts, full sets) | 150–300 | ~0 to 0.05% | **~0 to +0.4** | **−0.5 to +2.5**, mass on the floor | stays under ~1%, often 0.00 on the page | **do not use OLS** |
| Small optional (one race, try each activity, one robbery) | 1–8 | like early, a bit lower | **+0.8** | **0 to +2.0** | 1.8–3× | **~0.8** |
| Medium counters (dozens of vehicles, challenges, scans) | many sessions | 0.1–3% | **+0.7** | **−0.3 to +2.0** | 1.5–3× | **~0.7** |

Reading the early-gate row against the live game: Chapter 1 was already 12% at ~40 h and still steep. Center **+1.0** from a Saturday-morning rate in the teens lands near the high 20s to ~40% by Wednesday night, not near 90%. The +2.2 end of the band is “the Friday burst was the real slope, and the weekend matches it.” The +0.2 end is “tracked N doubles again and the easy cohort is already through.”

Late story and platinum need **heavy upper tails**. One guide wave or a few dozen hunters moves a 0.1% trophy by a full logit. The lower tail includes “Exophase prints 0.00 until the next refresh, and the refresh adds players faster than finishers.” Scoring clamps 0 and 100 to 0.01 and 99.99, so a platinum that is still 0.00 is a logit of **−9.2**. A forecast piled on 0.00 with a tiny band loses if a handful of profiles sync.

**Regime, not a single slope.** Spider-Man and Elden Ring say the logit-vs-log-time slope **shrinks as `r` leaves the single digits**. A trophy at 40% should not get the same `Δ` as a trophy at 1%. The house curve cannot express that: it fits one line per trophy on the last 24 h. Those 24 h, before Saturday morning US, are a weekday-plus-Friday-night sample, and Exophase often repeats the same counts for hours, so “24 h of reads” may be **3–8 distinct points**. Under 3 distinct reads the house curve *is* persistence. A steep Chapter 1 line estimated on the 20 Nov burst (slope ~3.5) is the main way that baseline overshoots.

House persistence at this horizon is already wide: `0.5 × √4.52 × 1.645 ≈ ±1.75 logit` at 5/95 (about 1.1% → 0.19–6.0). Beating it is mostly a **better median**. Coverage still wants a 90% band at least that wide on late and zero-ish trophies, and wider where the class says the weekend can jump. Narrowing early-gate bands below ~±1.3 logit is how a 0.83-coverage forecast loses to a wide one.

Practical shrinkage, as a prior not a fitted rule: take the persistence median, add the class `Δ` above, and pull a one-trophy log-time slope toward the class slope when the last day has few distinct refreshes or the fitted slope is outside the 5–95% column. Keep the random-walk width, and add extra width for platinum, 100%, and any trophy still under ~0.3%.

## Sources

- Spider-Man 2 week 1: https://www.pushsquare.com/news/2023/10/spider-man-2-is-already-doing-an-amazing-job-of-keeping-people-playing-on-ps5 ; https://www.ali213.net/news/html/2023-10/791125.html ; JorRaptor figures quoted at https://xgp.pl/newsy/spider-man-2-duzy-procent-graczy-ukonczylo-fabule/
- Spider-Man 2 mature Exophase / PSNProfiles: https://www.exophase.com/game/marvel-s-spider-man-2-psn/trophies/ ; https://psnprofiles.com/trophies/23918-marvels-spider-man-2
- Ragnarök ~day 15: https://www.pushsquare.com/news/2022/11/25percent-of-players-have-beaten-god-of-war-ragnarok-two-weeks-after-release ; https://www.truetrophies.com/n22384/god-of-war-ragnarok-trophies-epilogue ; hours: https://www.powerpyx.com/god-of-war-ragnarok-trophy-guide-roadmap/
- Elden Ring ~day 18: https://www.eurogamer.net/elden-rings-first-major-boss-defeated-by-70-percent-of-players ; week-2 deltas: https://www.gamepressure.com/newsroom/elden-ring-players-deal-with-bosses-fairly-easily/z44196 ; endings ~17% Steam: https://www.gamereactor.eu/three-weeks-after-launch-only-17-of-players-have-beat-elden-ring/
- RDR2 day ~48 (Reddit PSN paste, 11 Jan 2019): https://www.reddit.com/r/reddeadredemption/comments/aesc8c/read_the_text_alert_to_the_whole_community/ ; mature Exophase: https://www.exophase.com/game/red-dead-redemption-2-psn/trophies/ ; Sony vs site: https://psntrophyleaders.com/game/view/red-dead-redemption-2-ps4/ ; ~22% story by Jan 2019: https://www.gamereactor.se/bara-22-av-de-som-paborjat-red-dead-redemption-2-har-slutfort-det-705813/
- Hogwarts, late March 2023: https://www.netzwelt.de/news/215847-hogwarts-legacy-lediglich-34-prozent-aller-spieler-schliessen-geschichte-ab.html
- Cyberpunk first story unlocks: https://psnprofiles.com/trophy/11981-cyberpunk-2077/7-the-world
- Starfield early-access finishers: https://www.thegamer.com/starfield-900-players-beat-main-quest-early-access/
- GTA V first final-mission unlock: https://www.playstationtrophies.org/game/grand-theft-auto-5-ps4/trophy/99497-to-live-or-die-in-los-santos.html
- Exophase user base vs PSN: https://forums.exophase.com/threads/introducing-points-system-exp-and-cross-platform-leaderboards.45804/page-4 ; https://psn.gg/news/playstation-trophy-rarity-explained
- GTA VI length and chapters: https://outputlag.com/guides/gta-6-how-long-to-beat/ ; https://www.gamermarkt.com/blog/gta-6-how-long-to-beat/ ; https://duuro.net/blog/gta-6-missions-list-length ; https://noobs.es/guia/cuanto-dura-gta-6-horas-de-la-historia-capitulos-y-numero-de-misiones/ ; https://www.ign.com/articles/how-long-is-gta-6 ; platinum ~200 h: https://www.notebookcheck.net/Leak-says-GTA-6-story-takes-50-hours-to-complete-and-PS5-platinum-trophy-200-hours.1450952.0.html ; 100% not yet confirmed: https://outputlag.com/guides/gta-6-100-percent-completion/
- Unlock times: https://gta6launch.com/unlock-time ; https://www.gta6everything.com/questions/what-time-does-gta-6-unlock
- Sales: https://www.bbc.co.uk/news/articles/c9zr5nyv5dj2o ; https://www.gamesindustry.biz/sensor-tower-estimates-gta-6-generated-236bn-in-pre-order-and-launch-day-sales ; higher tracker: https://appgazers.com/reports/gta-6-revenue-sales-tracker
