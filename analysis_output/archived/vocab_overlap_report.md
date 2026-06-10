# 词汇重叠度分析报告 (FR+RA 56 章连贯 vs Reader)

> 视角: **FR+RA 是 LLPSI 主干教材的连贯系列 (1-56 章)**, 强推荐阈值 = 新词命中率 ≥ 30%
> 排除自身: `familia_romana` 和 `roma_aeterna` 不参与 reader 分析 (它们是参考系)。

## 一、整体覆盖度 (Reader 词表 vs FR+RA 56 章词表)

FR+RA 全 56 章词形数: **25,448** (FR 9,417 + RA 新增 16,031)

| Reader | 词数 | 覆盖FR+RA词 | 覆盖率 | FR+RA词占比 |
|:-------|-----:|------------:|-------:|------------:|
| `epitome_historiae_sacrae` | 10,698 | 5,300 | **20.8%** | 49.5% |
| `fabulae_syrae` | 8,546 | 4,877 | **19.2%** | 57.1% |
| `de_rerum_natura` | 9,134 | 4,333 | **17.0%** | 47.4% |
| `sermones_romani` | 8,089 | 3,651 | **14.3%** | 45.1% |
| `catilina` | 7,639 | 3,619 | **14.2%** | 47.4% |
| `ars_amatoria` | 7,109 | 3,165 | **12.4%** | 44.5% |
| `colloquia_personarum` | 4,129 | 2,418 | **9.5%** | 58.6% |
| `de_bello_gallico` | 8,264 | 2,192 | **8.6%** | 26.5% |
| `cena_trimalchionis` | 6,851 | 1,848 | **7.3%** | 27.0% |
| `fabellae_latinae` | 2,208 | 1,679 | **6.6%** | 76.0% |
| `amphitryo` | 5,033 | 1,590 | **6.2%** | 31.6% |
| `aeneis` | 773 | 360 | **1.4%** | 46.6% |

## 二、各章节组新词命中率 (按 6 组聚合)

**新词命中率** = (Reader 词表 ∩ 本章新词) / 本章新词数。
数值越高, 说明读完此章后立即读这本 reader, 越能高效巩固本章新词。

### FR 入门 (Cap. 1-7)

| Reader | Cap.1 | Cap.2 | Cap.3 | Cap.4 | Cap.5 | Cap.6 | Cap.7 | Avg |
|:-------|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|
| `epitome_historiae_sacrae` | 50.3% | 37.4% | 41.1% | 54.0% | 42.9% | 42.8% | 40.0% | **44.1%** |
| `fabulae_syrae` | 49.1% | 42.3% | 44.4% | 44.4% | 49.7% | 45.2% | 46.4% | **45.9%** |
| `de_rerum_natura` | 45.4% | 40.5% | 34.4% | 33.3% | 37.7% | 34.9% | 35.5% | **37.4%** |
| `sermones_romani` | 54.0% | 42.3% | 42.2% | 44.4% | 37.7% | 38.6% | 34.5% | **42.0%** |
| `catilina` | 44.8% | 31.3% | 24.4% | 31.0% | 34.3% | 33.1% | 28.2% | **32.4%** |
| `ars_amatoria` | 42.3% | 35.0% | 38.9% | 33.3% | 33.1% | 30.7% | 31.8% | **35.0%** |
| `colloquia_personarum` | 23.9% | 17.8% | 32.2% | 27.0% | 9.7% | 24.7% | 8.2% | **20.5%** |
| `de_bello_gallico` | 41.7% | 25.2% | 22.2% | 33.3% | 20.6% | 28.3% | 17.3% | **26.9%** |
| `cena_trimalchionis` | 36.2% | 25.8% | 31.1% | 35.7% | 22.9% | 24.1% | 19.1% | **27.8%** |
| `fabellae_latinae` | 57.7% | 47.9% | 51.1% | 54.8% | 55.4% | 46.4% | 55.5% | **52.7%** |
| `amphitryo` | 31.3% | 25.2% | 33.3% | 34.9% | 18.9% | 24.1% | 22.7% | **27.2%** |
| `aeneis` | 12.9% | 8.0% | 11.1% | 8.7% | 5.7% | 6.6% | 3.6% | **8.1%** |

### FR 进阶 A (Cap. 8-13)

| Reader | Cap.8 | Cap.9 | Cap.10 | Cap.11 | Cap.12 | Cap.13 | Avg |
|:-------|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|
| `epitome_historiae_sacrae` | 43.8% | 44.6% | 53.8% | 45.9% | 43.2% | 31.8% | **43.9%** |
| `fabulae_syrae` | 45.9% | 57.7% | 61.9% | 53.1% | 45.6% | 32.7% | **49.5%** |
| `de_rerum_natura` | 39.2% | 49.4% | 48.6% | 44.9% | 36.3% | 28.0% | **41.1%** |
| `sermones_romani` | 36.6% | 36.9% | 43.7% | 40.3% | 26.3% | 29.2% | **35.5%** |
| `catilina` | 34.5% | 19.6% | 33.2% | 29.6% | 33.6% | 22.6% | **28.9%** |
| `ars_amatoria` | 32.5% | 35.7% | 41.7% | 37.8% | 26.6% | 28.6% | **33.8%** |
| `colloquia_personarum` | 14.9% | 22.6% | 18.6% | 3.6% | 5.8% | 2.8% | **11.4%** |
| `de_bello_gallico` | 25.8% | 23.8% | 23.9% | 25.5% | 32.8% | 20.4% | **25.4%** |
| `cena_trimalchionis` | 24.7% | 22.6% | 28.7% | 32.7% | 17.8% | 15.4% | **23.7%** |
| `fabellae_latinae` | 47.9% | 39.3% | 36.0% | 36.7% | 29.0% | 24.8% | **35.6%** |
| `amphitryo` | 24.7% | 17.9% | 21.9% | 21.9% | 15.1% | 14.2% | **19.3%** |
| `aeneis` | 5.7% | 6.0% | 7.3% | 3.6% | 1.9% | 2.5% | **4.5%** |

### FR 进阶 B (Cap. 14-20)

| Reader | Cap.14 | Cap.15 | Cap.16 | Cap.17 | Cap.18 | Cap.19 | Cap.20 | Avg |
|:-------|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|
| `epitome_historiae_sacrae` | 40.9% | 35.4% | 31.6% | 28.7% | 30.7% | 30.6% | 32.6% | **32.9%** |
| `fabulae_syrae` | 39.6% | 37.0% | 41.8% | 24.3% | 26.4% | 42.6% | 28.6% | **34.3%** |
| `de_rerum_natura` | 37.8% | 29.8% | 33.1% | 21.5% | 25.5% | 27.8% | 22.7% | **28.3%** |
| `sermones_romani` | 40.4% | 35.9% | 22.1% | 21.5% | 31.4% | 25.1% | 23.4% | **28.5%** |
| `catilina` | 25.2% | 22.7% | 23.0% | 21.5% | 23.9% | 25.8% | 16.1% | **22.6%** |
| `ars_amatoria` | 29.1% | 27.1% | 22.4% | 14.2% | 21.1% | 25.1% | 23.7% | **23.2%** |
| `colloquia_personarum` | 8.3% | 11.0% | 7.5% | 18.6% | 3.1% | 11.3% | 8.2% | **9.7%** |
| `de_bello_gallico` | 22.6% | 16.0% | 18.2% | 15.8% | 14.3% | 11.7% | 12.5% | **15.9%** |
| `cena_trimalchionis` | 27.0% | 17.7% | 9.3% | 12.6% | 12.7% | 13.4% | 8.2% | **14.4%** |
| `fabellae_latinae` | 27.4% | 25.4% | 27.8% | 19.8% | 16.5% | 19.6% | 15.8% | **21.7%** |
| `amphitryo` | 21.7% | 17.1% | 11.0% | 10.1% | 10.6% | 11.3% | 11.2% | **13.3%** |
| `aeneis` | 5.2% | 5.0% | 2.4% | 1.2% | 0.9% | 2.7% | 1.6% | **2.7%** |

### FR 高阶 (Cap. 21-35)

| Reader | Cap.21 | Cap.22 | Cap.23 | Cap.24 | Cap.25 | Cap.26 | Cap.27 | Cap.28 | Cap.29 | Cap.30 | Cap.31 | Cap.32 | Cap.33 | Cap.34 | Cap.35 | Avg |
|:-------|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|
| `epitome_historiae_sacrae` | 33.3% | 34.1% | 30.1% | 31.5% | 32.3% | 34.1% | 29.9% | 31.2% | 31.7% | 29.7% | 29.5% | 28.0% | 24.9% | 16.2% | 15.4% | **28.8%** |
| `fabulae_syrae` | 33.8% | 33.0% | 28.9% | 35.1% | 39.5% | 3.8% | 10.3% | 12.9% | 5.5% | 10.8% | 20.2% | 8.8% | 12.5% | 4.9% | 7.2% | **17.8%** |
| `de_rerum_natura` | 25.7% | 26.9% | 22.6% | 25.2% | 24.1% | 29.1% | 25.6% | 20.6% | 18.2% | 23.5% | 23.3% | 20.6% | 14.9% | 19.6% | 15.4% | **22.3%** |
| `sermones_romani` | 28.8% | 25.8% | 21.8% | 23.4% | 21.8% | 21.2% | 21.1% | 15.8% | 20.0% | 29.4% | 17.3% | 19.9% | 14.6% | 16.8% | 13.3% | **20.7%** |
| `catilina` | 18.5% | 22.2% | 20.1% | 20.3% | 21.8% | 18.4% | 17.6% | 14.6% | 17.9% | 15.7% | 20.7% | 16.8% | 18.9% | 13.0% | 11.9% | **17.9%** |
| `ars_amatoria` | 23.0% | 21.1% | 17.6% | 23.0% | 19.5% | 23.1% | 19.3% | 9.4% | 16.9% | 14.4% | 17.6% | 15.4% | 10.8% | 17.2% | 8.2% | **17.1%** |
| `colloquia_personarum` | 14.0% | 7.2% | 4.2% | 7.7% | 6.4% | 6.6% | 6.5% | 4.3% | 2.9% | 7.2% | 5.4% | 3.1% | 3.1% | 4.0% | 8.5% | **6.1%** |
| `de_bello_gallico` | 11.7% | 16.8% | 10.5% | 11.7% | 10.5% | 14.4% | 14.6% | 6.7% | 7.3% | 9.2% | 10.2% | 10.0% | 12.7% | 5.3% | 6.8% | **10.6%** |
| `cena_trimalchionis` | 11.3% | 16.1% | 11.7% | 10.8% | 8.2% | 11.9% | 10.3% | 7.2% | 9.1% | 16.3% | 8.0% | 6.2% | 8.6% | 6.8% | 4.1% | **9.8%** |
| `fabellae_latinae` | 11.7% | 12.2% | 7.5% | 6.8% | 4.4% | 1.9% | 2.3% | 3.1% | 1.6% | 4.6% | 2.0% | 0.9% | 0.7% | 0.9% | 2.7% | **4.2%** |
| `amphitryo` | 14.0% | 16.5% | 13.8% | 10.8% | 10.3% | 7.8% | 6.5% | 7.0% | 4.9% | 8.2% | 7.1% | 7.8% | 6.2% | 7.0% | 5.8% | **8.9%** |
| `aeneis` | 3.6% | 4.7% | 2.1% | 1.4% | 1.8% | 1.2% | 1.5% | 1.0% | 1.0% | 3.3% | 0.3% | 0.9% | 1.7% | 1.1% | 0.3% | **1.7%** |

### RA 入门 (Cap. 36-42)

| Reader | Cap.36 | Cap.37 | Cap.38 | Cap.39 | Cap.40 | Cap.41 | Cap.42 | Avg |
|:-------|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|
| `epitome_historiae_sacrae` | 22.7% | 24.4% | 24.9% | 19.4% | 18.9% | 20.2% | 19.4% | **21.4%** |
| `fabulae_syrae` | 18.9% | 23.3% | 21.1% | 21.0% | 15.8% | 13.5% | 13.4% | **18.2%** |
| `de_rerum_natura` | 17.3% | 18.3% | 20.7% | 17.7% | 16.2% | 13.9% | 13.8% | **16.8%** |
| `sermones_romani` | 15.8% | 10.1% | 10.9% | 10.6% | 8.6% | 10.3% | 7.9% | **10.6%** |
| `catilina` | 17.4% | 9.5% | 10.7% | 11.6% | 9.6% | 9.5% | 13.1% | **11.6%** |
| `ars_amatoria` | 11.0% | 11.5% | 11.1% | 12.2% | 12.6% | 9.9% | 13.4% | **11.7%** |
| `colloquia_personarum` | 3.9% | 2.0% | 2.7% | 1.9% | 1.6% | 0.6% | 1.0% | **2.0%** |
| `de_bello_gallico` | 7.3% | 6.0% | 7.1% | 7.1% | 5.9% | 6.3% | 5.6% | **6.5%** |
| `cena_trimalchionis` | 7.3% | 3.8% | 6.2% | 4.9% | 5.5% | 3.6% | 3.2% | **4.9%** |
| `fabellae_latinae` | 1.5% | 0.8% | 0.7% | 0.9% | 0.5% | 0.2% | 0.5% | **0.7%** |
| `amphitryo` | 4.9% | 4.9% | 4.7% | 3.9% | 3.8% | 4.6% | 3.2% | **4.3%** |
| `aeneis` | 1.3% | 1.2% | 1.8% | 1.7% | 2.0% | 0.4% | 0.6% | **1.3%** |

### RA 高阶 (Cap. 43-56)

| Reader | Cap.43 | Cap.44 | Cap.45 | Cap.46 | Cap.47 | Cap.48 | Cap.49 | Cap.50 | Cap.51 | Cap.52 | Cap.53 | Cap.54 | Cap.55 | Cap.56 | Avg |
|:-------|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|
| `epitome_historiae_sacrae` | 16.7% | 13.6% | 12.8% | 12.7% | 10.0% | 9.6% | 13.7% | 10.5% | 9.6% | 9.2% | 6.9% | 7.5% | 9.1% | 5.7% | **10.6%** |
| `fabulae_syrae` | 10.3% | 7.1% | 7.6% | 7.5% | 3.2% | 6.1% | 7.9% | 6.4% | 4.1% | 5.1% | 3.9% | 5.6% | 3.8% | 6.3% | **6.1%** |
| `de_rerum_natura` | 13.4% | 10.8% | 8.4% | 7.1% | 11.2% | 7.1% | 9.1% | 8.0% | 6.8% | 9.7% | 6.4% | 6.3% | 7.9% | 10.5% | **8.8%** |
| `sermones_romani` | 8.9% | 6.9% | 6.9% | 6.8% | 6.8% | 6.2% | 5.7% | 4.8% | 5.2% | 6.0% | 5.3% | 4.8% | 5.4% | 5.4% | **6.1%** |
| `catilina` | 11.7% | 9.7% | 9.6% | 8.9% | 7.8% | 8.4% | 9.7% | 7.3% | 7.3% | 12.5% | 7.8% | 8.0% | 6.4% | 4.4% | **8.5%** |
| `ars_amatoria` | 7.7% | 6.9% | 6.8% | 5.3% | 2.9% | 4.7% | 2.8% | 3.9% | 4.4% | 4.3% | 2.8% | 2.5% | 2.6% | 4.4% | **4.4%** |
| `colloquia_personarum` | 1.3% | 1.0% | 1.2% | 0.7% | 3.7% | 0.6% | 0.6% | 1.1% | 1.0% | 0.9% | 0.8% | 0.3% | 0.6% | 0.6% | **1.0%** |
| `de_bello_gallico` | 6.0% | 5.0% | 3.5% | 5.0% | 2.4% | 4.7% | 5.1% | 4.0% | 2.6% | 4.6% | 2.0% | 2.8% | 2.2% | 1.7% | **3.7%** |
| `cena_trimalchionis` | 2.6% | 2.6% | 3.2% | 3.3% | 3.4% | 2.8% | 3.2% | 2.1% | 1.9% | 2.7% | 2.6% | 1.2% | 1.5% | 2.2% | **2.5%** |
| `fabellae_latinae` | 0.6% | 0.5% | 0.5% | 0.7% | 0.5% | 0.7% | 0.0% | 0.3% | 1.0% | 0.4% | 0.3% | 0.2% | 0.6% | 0.6% | **0.5%** |
| `amphitryo` | 2.6% | 1.8% | 2.8% | 1.4% | 2.0% | 1.9% | 1.4% | 1.4% | 1.0% | 2.1% | 1.7% | 0.9% | 1.9% | 0.9% | **1.7%** |
| `aeneis` | 1.0% | 0.1% | 0.4% | 0.2% | 0.0% | 0.4% | 1.0% | 0.1% | 0.2% | 0.2% | 0.2% | 0.1% | 0.0% | 0.6% | **0.3%** |

## 三、插入位置推荐 (新词命中率 ≥ 30%)

> **逻辑**: 当读者学完 Cap. N 后, 如果某本 reader 对 Cap. N 的新词命中率 ≥ 30%, 则该 reader 是 Cap. N 结束后的强推荐插入读物。
> **多本推荐**: 允许多本 reader 同时推荐 (如果都达到阈值), 给读者提供选择空间。

### 3.1 按章节视角 (哪一章后该读什么)

**有强推荐 reader 的章节** (新词命中率 ≥ 30%):

| 章节 | 强推荐 reader | 最佳命中详情 |
|:----:|:--------------|:-------------|
| Cap. 1 | `fabellae_latinae`, `sermones_romani`, `epitome_historiae_sacrae`, `fabulae_syrae`, `de_rerum_natura`, `catilina`, `ars_amatoria`, `de_bello_gallico`, `cena_trimalchionis`, `amphitryo` | `fabellae_latinae` 命中 94/163 (58%) |
| Cap. 2 | `fabellae_latinae`, `fabulae_syrae`, `sermones_romani`, `de_rerum_natura`, `epitome_historiae_sacrae`, `ars_amatoria`, `catilina` | `fabellae_latinae` 命中 78/163 (48%) |
| Cap. 3 | `fabellae_latinae`, `fabulae_syrae`, `sermones_romani`, `epitome_historiae_sacrae`, `ars_amatoria`, `de_rerum_natura`, `amphitryo`, `colloquia_personarum`, `cena_trimalchionis` | `fabellae_latinae` 命中 46/90 (51%) |
| Cap. 4 | `fabellae_latinae`, `epitome_historiae_sacrae`, `fabulae_syrae`, `sermones_romani`, `cena_trimalchionis`, `amphitryo`, `ars_amatoria`, `de_bello_gallico`, `de_rerum_natura`, `catilina` | `fabellae_latinae` 命中 69/126 (55%) |
| Cap. 5 | `fabellae_latinae`, `fabulae_syrae`, `epitome_historiae_sacrae`, `de_rerum_natura`, `sermones_romani`, `catilina`, `ars_amatoria` | `fabellae_latinae` 命中 97/175 (55%) |
| Cap. 6 | `fabellae_latinae`, `fabulae_syrae`, `epitome_historiae_sacrae`, `sermones_romani`, `de_rerum_natura`, `catilina`, `ars_amatoria` | `fabellae_latinae` 命中 77/166 (46%) |
| Cap. 7 | `fabellae_latinae`, `fabulae_syrae`, `epitome_historiae_sacrae`, `de_rerum_natura`, `sermones_romani`, `ars_amatoria` | `fabellae_latinae` 命中 61/110 (55%) |
| Cap. 8 | `fabellae_latinae`, `fabulae_syrae`, `epitome_historiae_sacrae`, `de_rerum_natura`, `sermones_romani`, `catilina`, `ars_amatoria` | `fabellae_latinae` 命中 93/194 (48%) |
| Cap. 9 | `fabulae_syrae`, `de_rerum_natura`, `epitome_historiae_sacrae`, `fabellae_latinae`, `sermones_romani`, `ars_amatoria` | `fabulae_syrae` 命中 97/168 (58%) |
| Cap. 10 | `fabulae_syrae`, `epitome_historiae_sacrae`, `de_rerum_natura`, `sermones_romani`, `ars_amatoria`, `fabellae_latinae`, `catilina` | `fabulae_syrae` 命中 153/247 (62%) |
| Cap. 11 | `fabulae_syrae`, `epitome_historiae_sacrae`, `de_rerum_natura`, `sermones_romani`, `ars_amatoria`, `fabellae_latinae`, `cena_trimalchionis` | `fabulae_syrae` 命中 104/196 (53%) |
| Cap. 12 | `fabulae_syrae`, `epitome_historiae_sacrae`, `de_rerum_natura`, `catilina`, `de_bello_gallico` | `fabulae_syrae` 命中 118/259 (46%) |
| Cap. 13 | `fabulae_syrae`, `epitome_historiae_sacrae` | `fabulae_syrae` 命中 104/318 (33%) |
| Cap. 14 | `epitome_historiae_sacrae`, `sermones_romani`, `fabulae_syrae`, `de_rerum_natura` | `epitome_historiae_sacrae` 命中 94/230 (41%) |
| Cap. 15 | `fabulae_syrae`, `sermones_romani`, `epitome_historiae_sacrae` | `fabulae_syrae` 命中 67/181 (37%) |
| Cap. 16 | `fabulae_syrae`, `de_rerum_natura`, `epitome_historiae_sacrae` | `fabulae_syrae` 命中 140/335 (42%) |
| Cap. 18 | `sermones_romani`, `epitome_historiae_sacrae` | `sermones_romani` 命中 101/322 (31%) |
| Cap. 19 | `fabulae_syrae`, `epitome_historiae_sacrae` | `fabulae_syrae` 命中 124/291 (43%) |
| Cap. 20 | `epitome_historiae_sacrae` | `epitome_historiae_sacrae` 命中 99/304 (33%) |
| Cap. 21 | `fabulae_syrae`, `epitome_historiae_sacrae` | `fabulae_syrae` 命中 75/222 (34%) |
| Cap. 22 | `epitome_historiae_sacrae`, `fabulae_syrae` | `epitome_historiae_sacrae` 命中 95/279 (34%) |
| Cap. 23 | `epitome_historiae_sacrae` | `epitome_historiae_sacrae` 命中 72/239 (30%) |
| Cap. 24 | `fabulae_syrae`, `epitome_historiae_sacrae` | `fabulae_syrae` 命中 78/222 (35%) |
| Cap. 25 | `fabulae_syrae`, `epitome_historiae_sacrae` | `fabulae_syrae` 命中 154/390 (39%) |
| Cap. 26 | `epitome_historiae_sacrae` | `epitome_historiae_sacrae` 命中 109/320 (34%) |
| Cap. 28 | `epitome_historiae_sacrae` | `epitome_historiae_sacrae` 命中 130/417 (31%) |
| Cap. 29 | `epitome_historiae_sacrae` | `epitome_historiae_sacrae` 命中 122/385 (32%) |

**无强推荐 reader 的章节** (新词命中率 < 30%, 缺少 reader 支撑):

- 章节范围: 17, 27, 30-56 (29 章)

| 章节 | 最高命中 reader | 最高命中率 |
|:----:|:----------------|:----------|
| Cap. 17 | `epitome_historiae_sacrae` | 28.7% (71/247) |
| Cap. 27 | `epitome_historiae_sacrae` | 29.9% (119/398) |
| Cap. 30 | `epitome_historiae_sacrae` | 29.7% (91/306) |
| Cap. 31 | `epitome_historiae_sacrae` | 29.5% (104/352) |
| Cap. 32 | `epitome_historiae_sacrae` | 28.0% (118/422) |
| Cap. 33 | `epitome_historiae_sacrae` | 24.9% (104/417) |
| Cap. 34 | `de_rerum_natura` | 19.6% (92/470) |
| Cap. 35 | `de_rerum_natura` | 15.4% (45/293) |
| Cap. 36 | `epitome_historiae_sacrae` | 22.7% (191/840) |
| Cap. 37 | `epitome_historiae_sacrae` | 24.4% (159/651) |
| Cap. 38 | `epitome_historiae_sacrae` | 24.9% (112/450) |
| Cap. 39 | `fabulae_syrae` | 21.0% (145/691) |
| Cap. 40 | `epitome_historiae_sacrae` | 18.9% (116/613) |
| Cap. 41 | `epitome_historiae_sacrae` | 20.2% (102/505) |
| Cap. 42 | `epitome_historiae_sacrae` | 19.4% (159/818) |
| Cap. 43 | `epitome_historiae_sacrae` | 16.7% (120/717) |
| Cap. 44 | `epitome_historiae_sacrae` | 13.6% (141/1034) |
| Cap. 45 | `epitome_historiae_sacrae` | 12.8% (110/857) |
| Cap. 46 | `epitome_historiae_sacrae` | 12.7% (112/879) |
| Cap. 47 | `de_rerum_natura` | 11.2% (46/409) |
| Cap. 48 | `epitome_historiae_sacrae` | 9.6% (145/1503) |
| Cap. 49 | `epitome_historiae_sacrae` | 13.7% (69/505) |
| Cap. 50 | `epitome_historiae_sacrae` | 10.5% (115/1094) |
| Cap. 51 | `epitome_historiae_sacrae` | 9.6% (59/616) |
| Cap. 52 | `catilina` | 12.5% (135/1077) |
| Cap. 53 | `catilina` | 7.8% (50/642) |
| Cap. 54 | `catilina` | 8.0% (72/904) |
| Cap. 55 | `epitome_historiae_sacrae` | 9.1% (62/685) |
| Cap. 56 | `de_rerum_natura` | 10.5% (57/541) |

### 3.2 按 Reader 视角 (这本 reader 适合在哪些章节后插入)

| Reader | 强推荐章节数 | 章节范围 | 适合的 LLPSI 阶段 |
|:-------|:------------:|:---------|:-----------------|
| `epitome_historiae_sacrae` | 27 | 1-16, 18-26, 28-29 | FR 入门 (Cap. 1-7), FR 进阶 A (Cap. 8-13), FR 进阶 B (Cap. 14-20), FR 高阶 (Cap. 21-35) |
| `fabulae_syrae` | 21 | 1-16, 19, 21-22, 24-25 | FR 入门 (Cap. 1-7), FR 进阶 A (Cap. 8-13), FR 进阶 B (Cap. 14-20), FR 高阶 (Cap. 21-35) |
| `de_rerum_natura` | 14 | 1-12, 14, 16 | FR 入门 (Cap. 1-7), FR 进阶 A (Cap. 8-13), FR 进阶 B (Cap. 14-20) |
| `sermones_romani` | 14 | 1-11, 14-15, 18 | FR 入门 (Cap. 1-7), FR 进阶 A (Cap. 8-13), FR 进阶 B (Cap. 14-20) |
| `ars_amatoria` | 11 | 1-11 | FR 入门 (Cap. 1-7), FR 进阶 A (Cap. 8-13) |
| `fabellae_latinae` | 11 | 1-11 | FR 入门 (Cap. 1-7), FR 进阶 A (Cap. 8-13) |
| `catilina` | 8 | 1-2, 4-6, 8, 10, 12 | FR 入门 (Cap. 1-7), FR 进阶 A (Cap. 8-13) |
| `cena_trimalchionis` | 4 | 1, 3-4, 11 | FR 入门 (Cap. 1-7), FR 进阶 A (Cap. 8-13) |
| `amphitryo` | 3 | 1, 3-4 | FR 入门 (Cap. 1-7) |
| `de_bello_gallico` | 3 | 1, 4, 12 | FR 入门 (Cap. 1-7), FR 进阶 A (Cap. 8-13) |
| `colloquia_personarum` | 1 | 3 | FR 入门 (Cap. 1-7) |

## 四、词汇缝隙警告

> 哪些章节的「新词」几乎没有任何 reader 命中 (阈值 < 10%)?

| 章节 | 最高新词覆盖 | 状态 | 最佳 reader |
|:----:|------------:|:-----|:------------|
| Cap. 48 | 9.6% | 🟡 弱覆盖 | `epitome_historiae_sacrae` |
| Cap. 51 | 9.6% | 🟡 弱覆盖 | `epitome_historiae_sacrae` |
| Cap. 53 | 7.8% | 🟡 弱覆盖 | `catilina` |
| Cap. 54 | 8.0% | 🟡 弱覆盖 | `catilina` |
| Cap. 55 | 9.1% | 🟡 弱覆盖 | `epitome_historiae_sacrae` |
