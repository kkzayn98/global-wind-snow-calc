// Continent metadata and country → continent mapping
const CONTINENT_INFO = {
    asia: { zh: "亚洲", en: "Asia", color: "#c9d6e3" },
    europe: { zh: "欧洲", en: "Europe", color: "#b8cfe0" },
    africa: { zh: "非洲", en: "Africa", color: "#d4c4a8" },
    north_america: { zh: "北美洲", en: "North America", color: "#b5d4c8" },
    south_america: { zh: "南美洲", en: "South America", color: "#c8ddb8" },
    oceania: { zh: "大洋洲", en: "Oceania", color: "#a8d4d4" },
};

const COUNTRY_CONTINENT = {
    jp: "asia", kr: "asia", in: "asia", sg: "asia", my: "asia", th: "asia", vn: "asia",
    ph: "asia", id: "asia", ae: "asia", sa: "asia", ir: "asia", il: "asia", pk: "asia",
    bd: "asia", kz: "asia", tw: "asia", hk: "asia", mo: "asia", mm: "asia", kh: "asia",
    mn: "asia", qa: "asia", kw: "asia", tr: "asia", lk: "asia",
    de: "europe", fr: "europe", gb: "europe", it: "europe", es: "europe", nl: "europe",
    ch: "europe", se: "europe", no: "europe", ru: "europe", pl: "europe", ua: "europe",
    fi: "europe", dk: "europe", pt: "europe", gr: "europe", cz: "europe", at: "europe",
    be: "europe", ie: "europe", ro: "europe", hu: "europe", is: "europe",
    us: "north_america", ca: "north_america", mx: "north_america", cr: "north_america",
    pa: "north_america", cu: "north_america", jm: "north_america",
    br: "south_america", ar: "south_america", cl: "south_america", co: "south_america",
    pe: "south_america", uy: "south_america", ve: "south_america", ec: "south_america",
    bo: "south_america", py: "south_america",
    eg: "africa", za: "africa", ng: "africa", ke: "africa", ma: "africa", gh: "africa",
    tz: "africa", et: "africa",
    au: "oceania", nz: "oceania", fj: "oceania",
};
