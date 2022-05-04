from structures import SzkicTechnicznyKKTJ, Epimenidas, Link, Geocache, Wikipedia

PRELOAD_IMAGES = [11098, 1989, 1990, 2064, 2050, 1227, 1445, 2077, 1197, 2170, 1473, 1535, 1472, 1187, 490, 1245, 1537, 491]

DATA = {
	# Jaskinia Wielka Śnieżna / T-Wielka Śnieżna
	490: [
        SzkicTechnicznyKKTJ('t-wielka_sniezna'),
        Epimenidas('tatry/sniezn_p'),
        Wikipedia('Jaskinia_Wielka_Śnieżna'),
    ],

	# Jaskinia Wielka Litworowa / T.E-12.01
	491: [
        SzkicTechnicznyKKTJ('t-wielka_litworowa'),
        Epimenidas('tatry/sniezn_p'),
        Wikipedia('Jaskinia_Wielka_Śnieżna'),
    ],

	# Jaskinia Zimna / T.D-08.08
	1095: [
        SzkicTechnicznyKKTJ('t-zimna')
    ],

	# Jaskinia Miętusia Wyżnia / T.D-10.01
	1187: [
        SzkicTechnicznyKKTJ('t-mietusia_wyz'),
        Epimenidas('tatry/miewyz_p'),
        Wikipedia('Jaskinia_Miętusia_Wyżnia'),
    ],

	# Jaskinia Miętusia / T.D-11.01
	1197: [
        SzkicTechnicznyKKTJ('t-mietusia')
    ],

	# Jaskinia Błotna / T.D-12.05
	1213: [
        SzkicTechnicznyKKTJ('j-blotna')
    ],

	# Jaskinia Kasprowa Niżnia / T.D-16.03
	1227: [
        SzkicTechnicznyKKTJ('t-kasprowa_niz')
    ],

	# Jaskinia Kasprowa Wyżnia / T.D-17.01
	1245: [
        SzkicTechnicznyKKTJ('t-kasprowa_sr_wyz'),
        Epimenidas('tatry/kaswyz'),
        Wikipedia('Jaskinia_Kasprowa_Wyżnia'),
    ],

	# Jaskinia Kasprowa Średnia / T.D-17.02
	1247: [
        SzkicTechnicznyKKTJ('t-kasprowa_sr_wyz'),
        Epimenidas('tatry/kassr'),
        Wikipedia('Jaskinia_Kasprowa_Średnia'),
    ],

	# Jaskinia Czarna / T.E-09.12
	1445: [
        SzkicTechnicznyKKTJ('t-czarna'),
        Epimenidas('tatry/czarna_p'),
        Wikipedia('Jaskinia_Czarna'),
    ],

	# Jaskinia Marmurowa / T.E-11.05
	1472: [
        SzkicTechnicznyKKTJ('t-marmurowa'),
        Epimenidas('tatry/marmur_p'),
        Wikipedia('Jaskinia_Marmurowa'),
    ],

	# Ptasia Studnia / T.E-11.06
	1473: [
        SzkicTechnicznyKKTJ('t-ptasia_stud-lod_litw'),
        Epimenidas('tatry/ptasiastudnia_p'),
        Wikipedia('Ptasia_Studnia'),
    ],

	# Jaskinia nad Dachem / T.E-11.09
	1474: [
        SzkicTechnicznyKKTJ('t-nad_dachem')
    ],

	# Jaskinia pod Dachem / T.E-11.08
	1477: [
        SzkicTechnicznyKKTJ('t-pod_dachem')
    ],

	# Jaskinia Kozia / T.E-11.11
	1478: [
        SzkicTechnicznyKKTJ('t-kozia')
    ],

	# Studnia w Kazalnicy / T.E-11.12
	1480: [
        SzkicTechnicznyKKTJ('t-studnia_w_kazalnicy')
    ],

	# Studnia za Murem / T.E-11.13
	1482: [
        SzkicTechnicznyKKTJ('t-studnia_za_murem')
    ],

	# Jaskinia Lodowa w Twardych Spadach / T.E-11.44
	1507: [
        SzkicTechnicznyKKTJ('t-lodowa_twarde_spady')
    ],


	# Niebieska Studnia / T.E-12.02
	1533: [
        SzkicTechnicznyKKTJ('t-niebieska_studnia')
    ],


	# Jaskinia pod Wantą / T.E-12.03
	1535: [
        SzkicTechnicznyKKTJ('t-pod_wanta'),
        Epimenidas('tatry/podwanta_p'),
        Wikipedia('Jaskinia_pod_Wantą'),
    ],


	# Jaskinia Małołącka / T.E-12.07
	1537: [
        SzkicTechnicznyKKTJ('t-malolacka'),
        Epimenidas('tatry/mlacka_p'),
        Wikipedia('Jaskinia_Małołącka'),
    ],

	# Jaskinia Lodowa Małołącka / T.E-13.02
	1627: [
        Epimenidas('tatry/lodmal_p'),
        Wikipedia('Jaskinia_Lodowa_Małołącka'),
    ],


	# Jaskinia Małotowa / J.Olk.I-07.27
	1978: [
        SzkicTechnicznyKKTJ('j-malotowa')
    ],


	# Jaskinia nad Źródłem I / J.Olk.I-07.29
	1989: [
        SzkicTechnicznyKKTJ('j-nad_zrodlem1')
    ],


	# Jaskinia Łabajowa / J.Olk.I-07.46
	2030: [
        SzkicTechnicznyKKTJ('j-labajowa1_2')
    ],

	# Jaskinia Twardowskiego / J.BK-02.10
	2077: [
        Link('Plan i przekrój (wysoka rozdzielczość)', 'http://kktj.pl/Portals/0/EasyGalleryImages/5/73/twardowskiego1.jpg')
    ],

	# Wiercica / J.Cz.I-05.55
	2519: [
        SzkicTechnicznyKKTJ('j-wiercica')
    ],


	# Jaskinia Harda / T.E-11.71
	4866: [
        SzkicTechnicznyKKTJ('t-harda')
    ],

	# Jaskinia Twarda / J.Olk.II-03.29
	10430: [
        SzkicTechnicznyKKTJ('j-twarda')
    ],


	# Jaskinia Racławicka / J.Olk.I-09.39
	11098: [
        SzkicTechnicznyKKTJ('j-raclawicka'),
        Epimenidas('jura/raclaw_p'),
        Wikipedia('Jaskinia_Racławicka'),
        Link('Jaskinie Jury', 'http://www.jaskiniejury.pl/jaskinie-wyzyny/132-raclawicka'),
        Geocache('GC5RKVY'),
    ],

	# Szeroki Awen / J.Olk.I-08.108
	11221: [
        SzkicTechnicznyKKTJ('j-szeroki_aven')
    ],
}


if __name__ == '__main__':
    for key, links in DATA.items():
        for link in links:
            print(link, isinstance(link, Link))
            if isinstance(link, Link):
                link.validate()
