#!/usr/bin/env python3
"""
LLPSI OCR & 词表 第二轮精准修复
- 修复OCR文本中的已知过度拆分模式
- 重建参考词典
- 清理词表残留碎片
- 修复粘合词
"""

import json
import re
from pathlib import Path
from collections import Counter

BASE = Path("/Users/max/Downloads/Projects/LLPSI_plus")
VOCAB_DIR = BASE / "difficulty_algorithm" / "vocab_by_chapter"
OCR_DIR = BASE / "OCR"

# ═══════════════════════════════════════════════════════════
# 已知的OCR过度拆分模式（空格误插入）
# ═══════════════════════════════════════════════════════════
OVERSPLIT_PATTERNS = [
    # 常见被拆分的拉丁词
    (r'\bquo que\b', 'quoque'),
    (r'\bquo dam\b', 'quodam'),
    (r'\bflu vius\b', 'fluvius'),
    (r'\bflu vii\b', 'fluvii'),
    (r'\bflu vios\b', 'fluvios'),
    (r'\bflu vium\b', 'fluvium'),
    (r'\bflu vio\b', 'fluvio'),
    (r'\bpar vus\b', 'parvus'),
    (r'\bpar va\b', 'parva'),
    (r'\bpar vi\b', 'parvi'),
    (r'\bpar vum\b', 'parvum'),
    (r'\bpar vae\b', 'parvae'),
    (r'\bpar vos\b', 'parvos'),
    (r'\bpar vorum\b', 'parvorum'),
    (r'\bpar varum\b', 'parvarum'),
    (r'\bpar vis\b', 'parvis'),
    (r'\binsu la\b', 'insula'),
    (r'\binsu lae\b', 'insulae'),
    (r'\binsu lam\b', 'insulam'),
    (r'\binsu las\b', 'insulas'),
    (r'\binsu larum\b', 'insularum'),
    (r'\binsu lis\b', 'insulis'),
    (r'\bnum erus\b', 'numerus'),
    (r'\bnum eri\b', 'numeri'),
    (r'\bnum erum\b', 'numerum'),
    (r'\bnum eris\b', 'numeris'),
    (r'\bnum erorum\b', 'numerorum'),
    (r'\bnum eros\b', 'numeros'),
    (r'\blitte ra\b', 'littera'),
    (r'\blitte rae\b', 'litterae'),
    (r'\blitte ram\b', 'litteram'),
    (r'\blitte ras\b', 'litteras'),
    (r'\blitte ris\b', 'litteris'),
    (r'\blitte rarum\b', 'litterarum'),
    (r'\bdomi nus\b', 'dominus'),
    (r'\bdomi ni\b', 'domini'),
    (r'\bdomi num\b', 'dominum'),
    (r'\bdomi no\b', 'domino'),
    (r'\bdomi nos\b', 'dominos'),
    (r'\bdomi norum\b', 'dominorum'),
    (r'\bdomi na\b', 'domina'),
    (r'\bdomi nae\b', 'dominae'),
    (r'\bdomi nam\b', 'dominam'),
    (r'\bepi stula\b', 'epistula'),
    (r'\bepi stulae\b', 'epistulae'),
    (r'\bepi stulam\b', 'epistulam'),
    (r'\bancil la\b', 'ancilla'),
    (r'\bancil lae\b', 'ancillae'),
    (r'\bancil lam\b', 'ancillam'),
    (r'\bancil las\b', 'ancillas'),
    (r'\bpuell a\b', 'puella'),
    (r'\bpuell ae\b', 'puellae'),
    (r'\bpuell am\b', 'puellam'),
    (r'\bpuell as\b', 'puellas'),
    (r'\bpuell arum\b', 'puellarum'),
    (r'\bpuell is\b', 'puellis'),
    (r'\bvocabu lum\b', 'vocabulum'),
    (r'\bvocabu la\b', 'vocabula'),
    (r'\bvocabu li\b', 'vocabuli'),
    (r'\bvocabu lo\b', 'vocabulo'),
    (r'\bvocabu lis\b', 'vocabulis'),
    (r'\bvocabu lorum\b', 'vocabulorum'),
    (r'\bcapitu lum\b', 'capitulum'),
    (r'\bcapitu la\b', 'capitula'),
    (r'\bcapitu li\b', 'capituli'),
    (r'\bcapitu lo\b', 'capitulo'),
    (r'\bcapitu lis\b', 'capitulis'),
    (r'\bexem plum\b', 'exemplum'),
    (r'\bexem pla\b', 'exempla'),
    (r'\bexem pli\b', 'exempli'),
    (r'\bexem plo\b', 'exemplo'),
    (r'\bexem plis\b', 'exemplis'),
    (r'\bexem plorum\b', 'exemplorum'),
    (r'\bprovin cia\b', 'provincia'),
    (r'\bprovin ciae\b', 'provinciae'),
    (r'\bprovin ciam\b', 'provinciam'),
    (r'\bprovin cias\b', 'provincias'),
    (r'\bprovin ciarum\b', 'provinciarum'),
    (r'\bprovin ciis\b', 'provinciis'),
    (r'\bimpe rium\b', 'imperium'),
    (r'\bimpe rii\b', 'imperii'),
    (r'\bimpe rio\b', 'imperio'),
    (r'\bmag nus\b', 'magnus'),
    (r'\bmag na\b', 'magna'),
    (r'\bmag num\b', 'magnum'),
    (r'\bmag ni\b', 'magni'),
    (r'\bmag nae\b', 'magnae'),
    (r'\bmag nos\b', 'magnos'),
    (r'\bmag nas\b', 'magnas'),
    (r'\bmag norum\b', 'magnorum'),
    (r'\bmag narum\b', 'magnarum'),
    (r'\bmag nis\b', 'magnis'),
    (r'\bstatim que\b', 'statimque'),
    (r'\bne que\b', 'neque'),
    (r'\bat que\b', 'atque'),
    (r'\bita que\b', 'itaque'),
    (r'\busi que\b', 'usique'),
    (r'\bun dique\b', 'undique'),
    (r'\buter que\b', 'uterque'),
    (r'\bplerum que\b', 'plerumque'),
    (r'\bplerique\b', 'plerique'),  # already correct, skip
    (r'\bplerumque\b', 'plerumque'),  # already correct, skip
    (r'\bquis que\b', 'quisque'),
    (r'\bunusquis que\b', 'unusquisque'),
    (r'\bquis quis\b', 'quisquis'),
    (r'\bquicum que\b', 'quicumque'),
    (r'\bquae que\b', 'quaeque'),
    (r'\bquod que\b', 'quodque'),
    (r'\bquam que\b', 'quamque'),
    (r'\bquem que\b', 'quemque'),
    (r'\bquos que\b', 'quosque'),
    (r'\bquas que\b', 'quasque'),
    (r'\bquibus que\b', 'quibusque'),
    (r'\bquibuscum que\b', 'quibuscumque'),
    (r'\bunus quisque\b', 'unusquisque'),
    (r'\bunum quemque\b', 'unumquemque'),
    (r'\bunius cuiusque\b', 'uniuscuiusque'),
    (r'\buni cuique\b', 'unicuique'),
    (r'\bdeni que\b', 'denique'),
    (r'\bdein de\b', 'deinde'),
    (r'\bexin de\b', 'exinde'),
    (r'\bperin de\b', 'perinde'),
    (r'\bproin de\b', 'proinde'),
    (r'\bsubin de\b', 'subinde'),
    (r'\bante quam\b', 'antequam'),
    (r'\bpost quam\b', 'postquam'),
    (r'\bprius quam\b', 'priusquam'),
    (r'\bnum quam\b', 'numquam'),
    (r'\bum quam\b', 'umquam'),
    (r'\bus quam\b', 'usquam'),
    (r'\bquis quam\b', 'quisquam'),
    (r'\bquic quam\b', 'quicquam'),
    (r'\bne quis\b', 'nequis'),
    (r'\bne quid\b', 'nequid'),
    (r'\bsi quis\b', 'siquis'),
    (r'\bsi quid\b', 'siquid'),
    (r'\bnum quis\b', 'numquis'),
    (r'\bnum quid\b', 'numquid'),
    (r'\bec quis\b', 'ecquis'),
    (r'\bec quid\b', 'ecquid'),
    (r'\bali quis\b', 'aliquis'),
    (r'\bali quid\b', 'aliquid'),
    (r'\bali qua\b', 'aliqua'),
    (r'\bali quod\b', 'aliquod'),
    (r'\bali quem\b', 'aliquem'),
    (r'\bali quam\b', 'aliquam'),
    (r'\bali quo\b', 'aliquo'),
    (r'\bali quos\b', 'aliquos'),
    (r'\bali quas\b', 'aliquas'),
    (r'\bali quibus\b', 'aliquibus'),
    (r'\bali quorum\b', 'aliquorum'),
    (r'\bali quarum\b', 'aliquarum'),
    (r'\bquid dam\b', 'quiddam'),
    (r'\bquae dam\b', 'quaedam'),
    (r'\bqui dam\b', 'quidam'),
    (r'\bquod dam\b', 'quoddam'),
    (r'\bquem dam\b', 'quemdam'),
    (r'\bquam dam\b', 'quamdam'),
    (r'\bquo dam\b', 'quodam'),
    (r'\bquos dam\b', 'quosdam'),
    (r'\bquas dam\b', 'quasdam'),
    (r'\bquibus dam\b', 'quibusdam'),
    (r'\bquorum dam\b', 'quorumdam'),
    (r'\bquarum dam\b', 'quarumdam'),
    (r'\bquon dam\b', 'quondam'),
    (r'\bet iam\b', 'etiam'),
    (r'\biam que\b', 'iamque'),
    (r'\bubi que\b', 'ubique'),
    (r'\bun de\b', 'unde'),
    (r'\bin de\b', 'inde'),
    (r'\btam en\b', 'tamen'),
    (r'\battam en\b', 'attamen'),
    (r'\bverum tam en\b', 'verumtamen'),
    (r'\baut em\b', 'autem'),
    (r'\ben im\b', 'enim'),
    (r'\bquon iam\b', 'quoniam'),
    (r'\bi gitur\b', 'igitur'),
    (r'\binter im\b', 'interim'),
    (r'\bpraeter ea\b', 'praeterea'),
    (r'\bpropter ea\b', 'propterea'),
    (r'\binter ea\b', 'interea'),
    (r'\bpost ea\b', 'postea'),
    (r'\bante a\b', 'antea'),
    (r'\bcontra \b(?!ea\b)', 'contra '),  # skip, too broad
    (r'\bid circo\b', 'idcirco'),
    (r'\bide o\b', 'ideo'),
    (r'\bad eo\b', 'adeo'),
    (r'\bprope rea\b', 'proprea'),  # might not exist
    # 常见被拆分的其他词
    (r'\bGer mania\b', 'Germania'),
    (r'\bGer maniae\b', 'Germaniae'),
    (r'\bGer maniam\b', 'Germaniam'),
    (r'\bBritan nia\b', 'Britannia'),
    (r'\bBritan niae\b', 'Britanniae'),
    (r'\bBrundi sium\b', 'Brundisium'),
    (r'\bBrundi sii\b', 'Brundisii'),
    (r'\bBrundi sio\b', 'Brundisio'),
    (r'\bTuscu lum\b', 'Tusculum'),
    (r'\bTuscu li\b', 'Tusculi'),
    (r'\bSardi nia\b', 'Sardinia'),
    (r'\bSardi niae\b', 'Sardiniae'),
    (r'\bSicil ia\b', 'Sicilia'),
    (r'\bSicil iae\b', 'Siciliae'),
    (r'\bHisp ania\b', 'Hispania'),
    (r'\bHisp aniae\b', 'Hispaniae'),
    (r'\bRho danus\b', 'Rhodanus'),
    (r'\bRho dani\b', 'Rhodani'),
    (r'\bDa nuvius\b', 'Danuvius'),
    (r'\bDa nuvii\b', 'Danuvii'),
    (r'\bTibe ris\b', 'Tiberis'),
    (r'\bCapitoli um\b', 'Capitolium'),
    (r'\bCapitoli i\b', 'Capitolii'),
    (r'\bPalati um\b', 'Palatium'),
    (r'\bPalati i\b', 'Palatii'),
    (r'\bAventi num\b', 'Aventinum'),
    (r'\bAventi ni\b', 'Aventini'),
    (r'\bCae li us\b', 'Caelius'),
    (r'\bCae li i\b', 'Caelii'),
    (r'\bCam pania\b', 'Campania'),
    (r'\bCam paniae\b', 'Campaniae'),
    (r'\bApu lia\b', 'Apulia'),
    (r'\bApu liae\b', 'Apuliae'),
    (r'\bCale ria\b', 'Caleria'),
    (r'\bCale riae\b', 'Caleriae'),
    (r'\bGrae cia\b', 'Graecia'),
    (r'\bGrae ciae\b', 'Graeciae'),
    (r'\bGrae ciam\b', 'Graeciam'),
    (r'\bAegyp tus\b', 'Aegyptus'),
    (r'\bAegyp ti\b', 'Aegypti'),
    (r'\bAegyp tum\b', 'Aegyptum'),
    (r'\bAegyp to\b', 'Aegypto'),
    (r'\bCartha go\b', 'Carthago'),
    (r'\bCartha ginis\b', 'Carthaginis'),
    (r'\bCartha gine\b', 'Carthagine'),
    (r'\bCartha ginem\b', 'Carthaginem'),
    (r'\bThes salia\b', 'Thessalia'),
    (r'\bThes saliae\b', 'Thessaliae'),
    (r'\bMace donia\b', 'Macedonia'),
    (r'\bMace doniae\b', 'Macedoniae'),
    (r'\bAra bia\b', 'Arabia'),
    (r'\bAra biae\b', 'Arabiae'),
    (r'\bAra biam\b', 'Arabiam'),
    (r'\bSy ria\b', 'Syria'),
    (r'\bSy riae\b', 'Syriae'),
    (r'\bSy riam\b', 'Syriam'),
    (r'\bAe milia\b', 'Aemilia'),
    (r'\bAe miliae\b', 'Aemiliae'),
    (r'\bAe miliam\b', 'Aemiliam'),
    (r'\bIu lia\b', 'Iulia'),
    (r'\bIu liae\b', 'Iuliae'),
    (r'\bIu liam\b', 'Iuliam'),
    (r'\bIu lius\b', 'Iulius'),
    (r'\bIu lii\b', 'Iulii'),
    (r'\bIu lium\b', 'Iulium'),
    (r'\bIu lio\b', 'Iulio'),
    (r'\bCorne lius\b', 'Cornelius'),
    (r'\bCorne lii\b', 'Cornelii'),
    (r'\bCorne lium\b', 'Cornelium'),
    (r'\bCorne lio\b', 'Cornelio'),
    (r'\bMar cus\b', 'Marcus'),
    (r'\bMar ci\b', 'Marci'),
    (r'\bMar cum\b', 'Marcum'),
    (r'\bMar co\b', 'Marco'),
    (r'\bQuin tus\b', 'Quintus'),
    (r'\bQuin ti\b', 'Quinti'),
    (r'\bQuin tum\b', 'Quintum'),
    (r'\bQuin to\b', 'Quinto'),
    (r'\bSex tus\b', 'Sextus'),
    (r'\bSex ti\b', 'Sexti'),
    (r'\bSex tum\b', 'Sextum'),
    (r'\bSex to\b', 'Sexto'),
    (r'\bTi tus\b', 'Titus'),
    (r'\bTi ti\b', 'Titi'),
    (r'\bTi tum\b', 'Titum'),
    (r'\bTi to\b', 'Tito'),
    (r'\bGai us\b', 'Gaius'),
    (r'\bGai i\b', 'Gaii'),
    (r'\bGai um\b', 'Gaium'),
    (r'\bGai o\b', 'Gaio'),
    (r'\bPub lius\b', 'Publius'),
    (r'\bPub lii\b', 'Publii'),
    (r'\bPub lium\b', 'Publium'),
    (r'\bPub lio\b', 'Publio'),
    (r'\bAp pius\b', 'Appius'),
    (r'\bAp pii\b', 'Appii'),
    (r'\bAp pium\b', 'Appium'),
    (r'\bAp pio\b', 'Appio'),
    (r'\bFla minius\b', 'Flaminius'),
    (r'\bFla minii\b', 'Flaminii'),
    (r'\bFla minium\b', 'Flaminium'),
    (r'\bFla minio\b', 'Flaminio'),
    (r'\bFla via\b', 'Flavia'),
    (r'\bFla viae\b', 'Flaviae'),
    (r'\bFla vius\b', 'Flavius'),
    (r'\bFla vii\b', 'Flavii'),
    (r'\bDo mitius\b', 'Domitius'),
    (r'\bDo mitii\b', 'Domitii'),
    (r'\bDo mitium\b', 'Domitium'),
    (r'\bDo mitio\b', 'Domitio'),
    (r'\bClau dius\b', 'Claudius'),
    (r'\bClau dii\b', 'Claudii'),
    (r'\bClau dium\b', 'Claudium'),
    (r'\bClau dio\b', 'Claudio'),
    (r'\bSer vius\b', 'Servius'),
    (r'\bSer vii\b', 'Servii'),
    (r'\bSer vium\b', 'Servium'),
    (r'\bSer vio\b', 'Servio'),
    (r'\bLau rentia\b', 'Laurentia'),
    (r'\bLau rentiae\b', 'Laurentiae'),
    (r'\bLau rentiam\b', 'Laurentiam'),
    (r'\bAu gustus\b', 'Augustus'),
    (r'\bAu gusti\b', 'Augusti'),
    (r'\bAu gustum\b', 'Augustum'),
    (r'\bAu gusto\b', 'Augusto'),
    (r'\bAu gusta\b', 'Augusta'),
    (r'\bAu gustae\b', 'Augustae'),
    (r'\bAu gustam\b', 'Augustam'),
    (r'\bCae sar\b', 'Caesar'),
    (r'\bCae saris\b', 'Caesaris'),
    (r'\bCae sari\b', 'Caesari'),
    (r'\bCae sarem\b', 'Caesarem'),
    (r'\bCae sare\b', 'Caesare'),
    (r'\bNepta nus\b', 'Neptanus'),
    (r'\bNepta ni\b', 'Neptani'),
    (r'\bMer curius\b', 'Mercurius'),
    (r'\bMer curii\b', 'Mercurii'),
    (r'\bMer curium\b', 'Mercurium'),
    (r'\bMer curio\b', 'Mercurio'),
    (r'\bAn tonius\b', 'Antonius'),
    (r'\bAn tonii\b', 'Antonii'),
    (r'\bAn tonium\b', 'Antonium'),
    (r'\bAn tonio\b', 'Antonio'),
    (r'\bAe ne as\b', 'Aeneas'),
    (r'\bAe ne ae\b', 'Aeneae'),
    (r'\bAe ne am\b', 'Aeneam'),
    (r'\bAe nea\b', 'Aenea'),
    (r'\bRomu lus\b', 'Romulus'),
    (r'\bRomu li\b', 'Romuli'),
    (r'\bRomu lum\b', 'Romulum'),
    (r'\bRomu lo\b', 'Romulo'),
    (r'\bRe mus\b', 'Remus'),
    (r'\bRe mi\b', 'Remi'),
    (r'\bRe mum\b', 'Remum'),
    (r'\bRe mo\b', 'Remo'),
    # 常见复合词
    (r'\bimpe rator\b', 'imperator'),
    (r'\bimpe ratoris\b', 'imperatoris'),
    (r'\bimpe ratori\b', 'imperatori'),
    (r'\bimpe ratorem\b', 'imperatorem'),
    (r'\bimpe ratore\b', 'imperatore'),
    (r'\bimpe ratores\b', 'imperatores'),
    (r'\bimpe ratorum\b', 'imperatorum'),
    (r'\bimpe ratoribus\b', 'imperatoribus'),
    (r'\bimpe rat\b', 'imperat'),
    (r'\bimpe rant\b', 'imperant'),
    (r'\bimpe ravit\b', 'imperavit'),
    (r'\bimpe raverunt\b', 'imperaverunt'),
    (r'\bimpe rare\b', 'imperare'),
    (r'\bimpe rari\b', 'imperari'),
    (r'\bimpe randum\b', 'imperandum'),
    (r'\bimpe rans\b', 'imperans'),
    (r'\bcha racter\b', 'character'),
    (r'\bcha racteres\b', 'characteres'),
    (r'\bphi losophia\b', 'philosophia'),
    (r'\bphi losophiae\b', 'philosophiae'),
    (r'\bphi losophiam\b', 'philosophiam'),
    (r'\bphi losophus\b', 'philosophus'),
    (r'\bphi losophi\b', 'philosophi'),
    (r'\bphi losophum\b', 'philosophum'),
    (r'\bphi losopho\b', 'philosopho'),
    (r'\bphi losophos\b', 'philosophos'),
    (r'\bphi losophorum\b', 'philosophorum'),
    (r'\bphi losophis\b', 'philosophis'),
    (r'\bRoma nus\b', 'Romanus'),
    (r'\bRoma ni\b', 'Romani'),
    (r'\bRoma num\b', 'Romanum'),
    (r'\bRoma no\b', 'Romano'),
    (r'\bRoma na\b', 'Romana'),
    (r'\bRoma nae\b', 'Romanae'),
    (r'\bRoma nam\b', 'Romanam'),
    (r'\bRoma nos\b', 'Romanos'),
    (r'\bRoma nas\b', 'Romanas'),
    (r'\bRoma norum\b', 'Romanorum'),
    (r'\bRoma narum\b', 'Romanarum'),
    (r'\bRoma nis\b', 'Romanis'),
    (r'\bGrae cus\b', 'Graecus'),
    (r'\bGrae ci\b', 'Graeci'),
    (r'\bGrae cum\b', 'Graecum'),
    (r'\bGrae co\b', 'Graeco'),
    (r'\bGrae ca\b', 'Graeca'),
    (r'\bGrae cae\b', 'Graecae'),
    (r'\bGrae cam\b', 'Graecam'),
    (r'\bGrae cos\b', 'Graecos'),
    (r'\bGrae cas\b', 'Graecas'),
    (r'\bGrae corum\b', 'Graecorum'),
    (r'\bGrae carum\b', 'Graecarum'),
    (r'\bGrae cis\b', 'Graecis'),
    (r'\bLati nus\b', 'Latinus'),
    (r'\bLati ni\b', 'Latini'),
    (r'\bLati num\b', 'Latinum'),
    (r'\bLati no\b', 'Latino'),
    (r'\bLati na\b', 'Latina'),
    (r'\bLati nae\b', 'Latinae'),
    (r'\bLati nam\b', 'Latinam'),
    (r'\bLati nos\b', 'Latinos'),
    (r'\bLati nas\b', 'Latinas'),
    (r'\bLati norum\b', 'Latinorum'),
    (r'\bLati narum\b', 'Latinarum'),
    (r'\bLati nis\b', 'Latinis'),
    (r'\bAfri ca\b', 'Africa'),
    (r'\bAfri cae\b', 'Africae'),
    (r'\bAfri cam\b', 'Africam'),
    (r'\bAfri ca\b', 'Africa'),
    (r'\bEuro pa\b', 'Europa'),
    (r'\bEuro pae\b', 'Europae'),
    (r'\bEuro pam\b', 'Europam'),
    (r'\bAsi a\b', 'Asia'),
    (r'\bAsi ae\b', 'Asiae'),
    (r'\bAsi am\b', 'Asiam'),
    (r'\bcapit ulum\b', 'capitulum'),
    (r'\bcapit ula\b', 'capitula'),
    (r'\bcapit uli\b', 'capituli'),
    (r'\bcapit ulo\b', 'capitulo'),
    (r'\bcapit ulis\b', 'capitulis'),
    (r'\bcapit ulorum\b', 'capitulorum'),
    (r'\bexerci tus\b', 'exercitus'),
    (r'\bexerci tus\b', 'exercitus'),
    (r'\bexerci tum\b', 'exercitum'),
    (r'\bexerci tui\b', 'exercitui'),
    (r'\bexerci tuum\b', 'exercituum'),
    (r'\bexerci tibus\b', 'exercitibus'),
    # 句号/逗号后接词的过度拆分（常见于行末）
    # 已经由行间断词修复处理，这里补充几个特殊情况
    (r'\baequ or\b', 'aequor'),
    (r'\baequ oris\b', 'aequoris'),
    (r'\baequ ori\b', 'aequori'),
    (r'\baequ ore\b', 'aequore'),
    (r'\baequ ora\b', 'aequora'),
    (r'\bcorp oris\b', 'corporis'),
    (r'\bcorp ori\b', 'corpori'),
    (r'\bcorp ore\b', 'corpore'),
    (r'\bcorp ora\b', 'corpora'),
    (r'\bcorp orum\b', 'corporum'),
    (r'\bcorp oribus\b', 'corporibus'),
    (r'\btemp oris\b', 'temporis'),
    (r'\btemp ori\b', 'tempori'),
    (r'\btemp ore\b', 'tempore'),
    (r'\btemp ora\b', 'tempora'),
    (r'\btemp orum\b', 'temporum'),
    (r'\btemp oribus\b', 'temporibus'),
    (r'\bpec toris\b', 'pectoris'),
    (r'\bpec tori\b', 'pectori'),
    (r'\bpec tore\b', 'pectore'),
    (r'\bpec tora\b', 'pectora'),
    (r'\bpec torum\b', 'pectorum'),
    (r'\bpec toribus\b', 'pectoribus'),
    (r'\bfem ina\b', 'femina'),
    (r'\bfem inae\b', 'feminae'),
    (r'\bfem inam\b', 'feminam'),
    (r'\bfem inas\b', 'feminas'),
    (r'\bfem inarum\b', 'feminarum'),
    (r'\bfem inis\b', 'feminis'),
    (r'\bnom inis\b', 'nominis'),
    (r'\bnom ini\b', 'nomini'),
    (r'\bnom ine\b', 'nomine'),
    (r'\bnom ina\b', 'nomina'),
    (r'\bnom inum\b', 'nominum'),
    (r'\bnom inibus\b', 'nominibus'),
    (r'\bflum inis\b', 'fluminis'),
    (r'\bflum ini\b', 'flumini'),
    (r'\bflum ine\b', 'flumine'),
    (r'\bflum ina\b', 'flumina'),
    (r'\bflum inum\b', 'fluminum'),
    (r'\bflum inibus\b', 'fluminibus'),
    (r'\blum inis\b', 'luminis'),
    (r'\blum ini\b', 'lumini'),
    (r'\blum ine\b', 'lumine'),
    (r'\blum ina\b', 'lumina'),
    (r'\blum inum\b', 'luminum'),
    (r'\blum inibus\b', 'luminibus'),
    (r'\bcarm inis\b', 'carminis'),
    (r'\bcarm ini\b', 'carmini'),
    (r'\bcarm ine\b', 'carmine'),
    (r'\bcarm ina\b', 'carmina'),
    (r'\bcarm inum\b', 'carminum'),
    (r'\bcarm inibus\b', 'carminibus'),
    (r'\bhom inis\b', 'hominis'),
    (r'\bhom ini\b', 'homini'),
    (r'\bhom ine\b', 'homine'),
    (r'\bhom ines\b', 'homines'),
    (r'\bhom inum\b', 'hominum'),
    (r'\bhom inibus\b', 'hominibus'),
    (r'\bvir gin is\b', 'virginis'),
    (r'\bvir gin i\b', 'virgini'),
    (r'\bvir gin e\b', 'virgine'),
    (r'\bvir gin es\b', 'virgines'),
    (r'\bvir gin um\b', 'virginum'),
    (r'\bvir gin ibus\b', 'virginibus'),
    (r'\bMar garita\b', 'Margarita'),
    (r'\bMar garitae\b', 'Margaritae'),
    (r'\bMar garitam\b', 'Margaritam'),
    (r'\bMar garitas\b', 'Margaritas'),
    (r'\bMar garitarum\b', 'Margaritarum'),
    (r'\bMar garitis\b', 'Margaritis'),
    # 没有空格的情况 - 这些由粘合词检测处理
]


def fix_ocr_oversplits(text):
    """修复OCR文本中的过度拆分"""
    changes = 0
    for pattern, replacement in OVERSPLIT_PATTERNS:
        new_text = re.sub(pattern, replacement, text)
        if new_text != text:
            # 只计算有实际变化的
            count = len(re.findall(pattern, text))
            changes += count
            text = new_text
    return text, changes


def fix_camel_glued(text):
    """修复大小写混合的粘合词"""
    changes = 0
    
    def fix_one(match):
        nonlocal changes
        word = match.group(0)
        # 跳过全大写缩写
        if word.isupper() and len(word) <= 3:
            return word
        parts = re.findall(r'[a-zāēīōūȳ]+|[A-ZĀĒĪŌŪȲ][a-zāēīōūȳ]*', word)
        if len(parts) >= 2:
            changes += 1
            return ' '.join(parts)
        return word
    
    text = re.sub(r'\b[a-zA-ZāēīōūȳĀĒĪŌŪȲ]{5,30}\b', fix_one, text)
    return text, changes


def main():
    print("=" * 60)
    print("LLPSI OCR & 词表 第二轮精准修复")
    print("=" * 60)
    
    # Step 1: 修复OCR文本中的过度拆分
    print("\nStep 1: 修复OCR过度拆分...")
    ocr_files = list(OCR_DIR.rglob("*.txt"))
    ocr_files = [f for f in ocr_files if f.name != "INDEX.md"]
    total_oversplit = 0
    total_camel = 0
    
    for fpath in sorted(ocr_files):
        text = fpath.read_text(encoding="utf-8", errors="replace")
        
        # 修复过度拆分
        text, oversplit_changes = fix_ocr_oversplits(text)
        total_oversplit += oversplit_changes
        
        # 修复粘合词
        text, camel_changes = fix_camel_glued(text)
        total_camel += camel_changes
        
        if oversplit_changes > 0 or camel_changes > 0:
            fpath.write_text(text, encoding="utf-8")
    
    print(f"  过度拆分修复: {total_oversplit} 处")
    print(f"  粘合词修复: {total_camel} 处")
    
    # Step 2: 重建参考词典
    print("\nStep 2: 重建参考词典...")
    word_counter = Counter()
    for fpath in ocr_files:
        try:
            text = fpath.read_text(encoding="utf-8", errors="replace")
            text = re.sub(r'\[\d+\]', ' ', text)
            words = re.findall(r'[a-zA-ZāēīōūȳĀĒĪŌŪȲ]+', text)
            for w in words:
                if len(w) >= 2:
                    word_counter[w.lower()] += 1
        except Exception as e:
            print(f"    警告: {fpath}: {e}")
    
    ref_dict = {w for w, c in word_counter.items() if c >= 2}
    print(f"  参考词典: {len(ref_dict)} 个词")
    
    # Step 3: 清理词表残留碎片
    print("\nStep 3: 清理词表残留碎片...")
    
    # 扩展的已知有效短词列表
    VALID_SHORT = {
        # 基础词
        'est','non','sed','iam','ubi','qui','cum','sum','quo','res','hic','hoc',
        'aer','aes','sol','pes','vox','dux','nix','lex','rex','pax','lux','bos',
        'flos','mos','ros','dos','os','ius','fas','vis','tus','sus','mus','cur',
        'cor','mar','par','vir','ter','per','sub','pro','prae','ab','ad','in',
        'ex','de','ob','ve','ne','si','ut','et','at','ac','id','is','ea','eo',
        'me','te','se','tu','su','da','do','em','no','ni','an','en','heu','vae',
        'ita','nam','tam','una','avia','ave','ala','ago','amo','ara','are','ars',
        'aut','bis','cui','deus','dies','domus','duo','ego','eae','eas','eos',
        'eum','ex','fas','fax','fur','gens','hac','huc','hunc','ibi','iis','imo',
        'ire','ite','lab','lar','lis','lux','manus','mare','mox','nec','nemo',
        'nil','nix','nunc','ole','ops','opus','ora','os','ovis','par','pax',
        'pes','pie','plebs','plus','pol','pos','pro','pubes','pus','qua','quae',
        'quam','quas','quem','quid','quis','quo','rem','res','rex','robur',
        'rus','sal','se','sed','sic','sin','sol','spe','spes','sto','sub',
        'sum','suus','tam','tres','tu','tum','tus','ubi','uda','udo','una',
        'vae','vas','vel','via','vim','vir','vis','vix','vox',
        'a','ab','ac','ad','an','at','aut','bis','cum','cur','da','de','do',
        'dum','e','en','eo','et','ex','fa','heu','hi','ia','id','in','io','is',
        'it','me','mi','ne','ni','ob','os','per','pro','qua','re','se','si',
        'sic','sub','sum','te','tu','ubi','ut','ve','vi',
        'cap','duo','num','una','sex','tres','CAP','unus','unde','mox','nil',
        'tum','aut','vel','nam','cur','qua','qui','nil','dum','hac','nunc',
        'i','ii','iii','iv','v','vi','vii','viii','ix','x','l','c','d','m',
        # 更多有效短词
        'mea','meo','meae','meus','meum','meos','meas','meis','meorum','mearum',
        'sua','suo','suae','suus','suum','suos','suas','suis','suorum','suarum',
        'tua','tuo','tuae','tuus','tuum','tuos','tuas','tuis','tuorum','tuarum',
        'aio','ais','ait','aiunt','aiebam','aiebas','aiebat','aiebant',
        'cio','cis','cit','ciunt','civi','citus','cieo',
        'eo','is','it','imus','itis','eunt','ibam','ibas','ibat','ibant',
        'edo','edis','edit','edimus','editis','edunt','edi','es','esse',
        'abs','ab','ex','de','pro','prae','sub','super','inter','circum',
        'ante','post','trans','per','ad','in','ob','propter','contra','apud',
        'extra','intra','supra','infra','ultra','citra','circa','erga','penes',
        'secundum','praeter','sine','tenus','coram','palam','clam',
        'ali','alius','alia','alium','alii','alio','alios','alias','aliorum',
        'con','col','com','cor','dis','dif','dir','re','red','se','sed',
        'arc','arx','ars','art','arx','arce','arcem','arces','arcium',
        'rat','rata','ratum','rati','ratae','ratos','ratas','reor','reri',
        'ser','sero','seris','serit','serimus','seritis','serunt','sevi','satum',
        'dit','dis','ditis','ditem','dites','ditior','ditissimus',
        'ent','ens','entis','enti','entem','entes','entia','entium','entibus',
        'ant','ans','antis','anti','antem','antes','antia','antium','antibus',
        'ber','beris','beri','bero','berum','beros','beris','beribus',
        'bit','bam','bat','bant','bo','bis','bit','bimus','bitis','bunt',
        'cad','cado','cadis','cadit','cadimus','caditis','cadunt','cecidi','casum',
        'cae','caes','caedis','caedit','caedimus','caeditis','caedunt','cecidi','caesum',
        'cet','cetus','ceti','ceto','cetum','cetos','cetorum','cetis',
        'lum','lim','lis','lumen','luminis','lumini','lumine','lumina','luminum',
        'phi','phii','phio','phium','phiorum',
        'rae','ra','raes','rae','ram','ras','rarum','ris',
        'flu','fluo','fluis','fluit','fluimus','fluitis','fluunt','fluxi','fluxum',
        'pul','pulch','pulcher','pulchra','pulchrum','pulchri','pulchrae',
        'tac','taceo','taces','tacet','tacemus','tacetis','tacent','tacui','tacitum',
        'lio','lien','lienis','lieni','lienem','lienes','lienum','lienibus',
        'Cūr',
        'aes','aeris','aeri','aerem','aere','aera','aerum','aeribus',
        'add','adde','addis','addit','addimus','additis','addunt','addidi','additum',
        'adv','adveho','advenio','adverto','advoco','advolo',
        'ama','amo','amas','amat','amamus','amatis','amant','amavi','amatum',
        'ami','amicus','amica','amici','amicae','amico','amicos','amicis',
        'bre','brev','brevis','breve','brevem','breves','brevia','brevium',
        'bet','beto','betis','betit','betimus','betitis','betunt',
        'ain','aine','aisne','aitne','aiuntne',
        'air','aira','airae','airam','airas','airarum','airis',
        'bal','balo','balas','balat','balamus','balatis','balant','balavi',
        'bum','bus','bubo','bubonis','buboni','bubonem','bubone','bubones',
        'par','paris','pari','parem','pares','parium','paribus',
        'vir','viri','viro','virum','viros','virorum','viris',
        'mar','maris','mari','mare','maria','marium','maribus',
        'cor','cordis','cordi','corem','corde','corda','cordium','cordibus',
        'vas','vasis','vasi','vasem','vase','vasa','vasorum','vasibus',
        'fur','furis','furi','furem','fure','fures','furum','furibus',
        'lar','laris','lari','larem','lare','lares','larum','laribus',
        'ops','opis','opi','opem','ope','opes','opum','opibus',
        'fa','fari','fatur','fabor','fabitur','fatus','fandi','fando',
        'ia','iam','ian','ianus','ianua','ianuae','ianuam','ianuas',
        'hi','hic','hiems','hiemis','hiemi','hiemem','hieme','hiemes',
        'io','ior','ius','ioris','iori','iorem','iore','iores','iorum',
        'mi','mihi','mei','meus','mea','meum','mei','meae','mei',
        'en','enim','ensis','ensem','ense','enses','ensium','ensibus',
        'fa','fax','facis','faci','facem','face','faces','facum','facibus',
        'pol','poll','polleo','polles','pollet','pollemus','polletis','pollent',
        'lab','labor','laberis','labitur','labimur','labuntur','lapsus',
        'ole','oleo','oles','olet','olemus','oletis','olent','olui',
        'pie','pius','pia','pium','pii','piae','pios','pias','piorum',
        'pubes','puberis','puberi','puberem','pubere','puberes','puberum',
        'robur','roboris','robori','roborem','robore','robora','roborum',
        'spe','spes','spei','spem','spe','spes','sperum','spebus',
        'uda','udus','uda','udum','udi','udae','udos','udas','udorum',
        'udo','udo','udare','udavi','udatum','udans','udandi','udando',
        'avi','avis','avi','avem','ave','aves','avium','avibus',
        'ave','aveo','aves','avet','avemus','avetis','avent',
        'ala','ala','alae','alam','alas','alarum','alis',
        'ago','agere','egi','actum','agens','agendi','agendo','agendum',
        'amo','amare','amavi','amatum','amans','amandi','amando','amandum',
        'ara','ara','arae','aram','aras','ararum','aris',
        'are','areo','ares','aret','aremus','aretis','arent','arui',
        'ars','artis','arti','artem','arte','artes','artium','artibus',
        'aut','autem','autumo','autumas','autumat','autumamus','autumatis','autumant',
        'bis','bis','bini','binae','bina','binos','binas','binorum',
        'cui','cuius','cui','quem','quo','qua','quibus','quorum','quarum',
        'eae','is','ea','eius','ei','eam','eo','ea','eae','earum','eis','eas',
        'eas','is','ea','eius','ei','eam','eo','ea','eae','earum','eis','eas',
        'eos','is','ea','eius','ei','eum','eo','ei','eos','eorum','eis','ea',
        'eum','is','ea','eius','ei','eum','eo','ei','eos','eorum','eis','ea',
        'gens','gentis','genti','gentem','gente','gentes','gentium','gentibus',
        'huc','hic','haec','hoc','huius','huic','hunc','hanc','hoc','hac','huc',
        'ire','eo','is','it','imus','itis','eunt','ire','iens','eundi','eundo',
        'ite','eo','is','it','imus','itis','eunt','ite','itote','eunto',
        'nunc','nunc','nunciam','nunciam','nunciam',
        'ole','olea','oleae','oleam','oleas','olearum','oleis',
        'plebs','plebis','plebi','plebem','plebe','plebes','plebium','plebibus',
        'plus','pluris','plures','plura','plurium','pluribus',
        'rem','res','rei','rem','re','res','rerum','rebus',
        'sal','salis','sali','salem','sale','sales','salium','salibus',
        'spe','spes','spei','spem','spe','spes','sperum','spebus',
        'sto','stare','steti','statum','stans','standi','stando','standum',
        'tus','tus','turis','turi','turem','ture','tura','turium','turibus',
        'sus','sus','suis','sui','suem','sue','sues','suum','subus',
        'udo','udus','uda','udum','udi','udae','udos','udas','udorum',
        'vas','vas','vadis','vadi','vadem','vade','vades','vadum','vadibus',
        'via','via','viae','viam','vias','viarum','viis',
        'vim','vis','vim','vi','vires','virium','viribus',
        'vix','vix','vixdum','vixdum',
        'eheu','io','heu','vae','ohe','eheu','eu','he','ha','ho','hu',
        'ah','oh','eh','ei','au','hui','phui','pro','vae','heu','eheu',
        'eho','eho','eho','eho','eho','eho','eho','eho',
    }
    
    # 需要在参考词典中出现的短词才保留
    # 对于3字母词：如果不在参考词典中，且在TRUNCATED_ROOTS中，删除
    # 对于3字母词：如果在参考词典中，保留
    # 对于4+字母词：使用原有逻辑
    
    LATIN_CHARS = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZāēīōūȳĀĒĪŌŪȲ")
    
    # 已知的无效短词碎片（包含3-4字母碎片）
    KNOWN_FRAGMENTS = {
        # 动词结尾碎片（不是独立词）
        'unt', 'ant', 'ent', 'bam', 'bat', 'bant', 'bit', 'bunt', 'eba',
        # 名词/形容词词根碎片
        'flu', 'phi', 'rae', 'lio', 'rat', 'dit', 'lum', 'pul', 'tac',
        'ari', 'art', 'bum', 'cad', 'cae', 'cet', 'dri', 'edi', 'con', 'arc',
        'ber', 'ces', 'air', 'bre', 'ain', 'ais', 'bet',
        'abs', 'add', 'adv', 'ama', 'ami', 'aes', 'bal', 'cio',
        'lam', 'lec', 'nit', 'tat', 'gem', 'mag', 'gat', 'den', 'dol', 'git',
        'fes', 'fra', 'cul', 'doc', 'col', 'cem', 'cog', 'cos', 'cir', 'dam',
        'cre', 'cas', 'med', 'tan', 'vio', 'ser', 'ere', 'eri', 'mae',
        'ali', 'bum', 'cad', 'cae', 'ces', 'con', 'dit',
        'bam', 'bat', 'bre', 'ain', 'ais', 'bet', 'add', 'adv', 'ama', 'ami',
    }
    
    def is_valid_short_word(w, ref_dict):
        """判断短词是否有效"""
        lower = w.lower()
        # 已知无效碎片（优先检查，因为参考词典可能被OCR污染）
        if lower in KNOWN_FRAGMENTS:
            return False
        # 如果在已知有效短词表中，有效
        if lower in VALID_SHORT:
            return True
        # 如果在参考词典中出现，大概率有效
        if lower in ref_dict:
            return True
        # 3-4字母且在参考词典中没出现 -> 大概率无效
        if len(w) <= 4 and lower not in ref_dict:
            return False
        return True
    
    vocab_files = sorted(VOCAB_DIR.glob("cap*_vocab_clean.json"))
    total_orig = 0
    total_clean = 0
    
    for fpath in vocab_files:
        chapter = re.search(r'cap(\d+)', fpath.name)
        ch = chapter.group(1) if chapter else "?"
        try:
            data = json.loads(fpath.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"    错误: {fpath}: {e}")
            continue
        
        original_count = len(data)
        cleaned = []
        seen = set()
        
        for word in data:
            w = word.strip()
            if not w:
                continue
            lower = w.lower()
            
            # 去重
            if lower in seen:
                continue
            
            # 检查是否是合法词
            if len(w) <= 4 and not is_valid_short_word(w, ref_dict):
                continue
            
            # 专有名词保留大写，其他小写
            # 如果在参考词典中以大写形式出现较多，可能是专有名词
            if w[0].isupper():
                # 检查是否作为专有名词出现
                if w in word_counter:
                    # 在OCR中以大写出现 → 保留大写
                    cleaned.append(w)
                elif lower in ref_dict:
                    # 在参考词典中以小写出现 → 小写化
                    cleaned.append(lower)
                else:
                    # 不在参考词典中 → 保留原样
                    cleaned.append(w)
            else:
                cleaned.append(lower)
            
            seen.add(lower)
        
        cleaned.sort(key=str.lower)
        fpath.write_text(json.dumps(cleaned, ensure_ascii=False, indent=2), encoding="utf-8")
        total_orig += original_count
        total_clean += len(cleaned)
        removed = original_count - len(cleaned)
        if removed > 0:
            print(f"  cap{ch}: {original_count} → {len(cleaned)} (删除 {removed} 条)")
    
    print(f"\n  词表总计: {total_orig} → {total_clean} (删除 {total_orig - total_clean} 条)")
    
    # Step 4: 重新生成 word_chapter_map.json
    print("\nStep 4: 重新生成 word_chapter_map.json...")
    word_chapter_map = {}
    for fpath in sorted(VOCAB_DIR.glob("cap*_vocab_clean.json")):
        chapter = re.search(r'cap(\d+)', fpath.name)
        if not chapter:
            continue
        ch = int(chapter.group(1))
        try:
            words = json.loads(fpath.read_text(encoding="utf-8"))
        except Exception:
            continue
        for word in words:
            w = word.lower()
            if w not in word_chapter_map:
                word_chapter_map[w] = []
            if ch not in word_chapter_map[w]:
                word_chapter_map[w].append(ch)
    
    wcm_path = BASE / "difficulty_algorithm" / "word_chapter_map.json"
    wcm_path.write_text(
        json.dumps(word_chapter_map, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
    print(f"  word_chapter_map.json: {len(word_chapter_map)} 个词条")
    
    print("\n" + "=" * 60)
    print("第二轮修复完成！")
    print(f"  OCR: 过度拆分 {total_oversplit} 处 + 粘合词 {total_camel} 处")
    print(f"  词表: {total_orig} → {total_clean}")
    print("=" * 60)


if __name__ == "__main__":
    main()