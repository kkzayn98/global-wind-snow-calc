#!/usr/bin/env node
/**
 * Build data/world-map.svg from Natural Earth 110m (world-atlas).
 * Groups countries into continents for interactive selection.
 */
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
import * as d3 from "d3";
import * as topojson from "topojson-client";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const root = path.join(__dirname, "..");
const topoPath = path.join(root, "scripts", "data", "countries-110m.json");
const outPath = path.join(root, "data", "world-map.svg");

/** ISO 3166-1 numeric id → continent */
const NUMERIC_CONTINENT = {
  "004": "asia", "008": "europe", "012": "africa", "016": "oceania",
  "020": "europe", "024": "africa", "028": "north_america", "031": "asia",
  "032": "south_america", "036": "oceania", "040": "europe", "044": "north_america",
  "048": "asia", "050": "asia", "051": "asia", "052": "north_america",
  "056": "europe", "060": "north_america", "064": "asia", "068": "south_america",
  "070": "europe", "072": "africa", "074": "europe", "076": "south_america",
  "084": "north_america", "086": "oceania", "090": "oceania", "092": "north_america",
  "096": "asia", "100": "europe", "104": "asia", "108": "africa",
  "112": "europe", "116": "asia", "120": "africa", "124": "north_america",
  "132": "africa", "140": "africa", "144": "asia", "148": "africa",
  "152": "south_america", "156": "asia", "158": "asia", "170": "south_america",
  "174": "africa", "178": "africa", "180": "africa", "188": "north_america",
  "191": "europe", "192": "north_america", "196": "europe", "203": "europe",
  "204": "africa", "208": "europe", "212": "north_america", "214": "north_america",
  "218": "south_america", "222": "north_america", "226": "africa", "231": "africa",
  "232": "africa", "233": "europe", "234": "europe", "238": "south_america",
  "242": "oceania", "246": "europe", "248": "europe", "250": "europe",
  "254": "south_america", "258": "oceania", "262": "africa", "266": "africa",
  "268": "asia", "270": "africa", "275": "asia", "276": "europe",
  "288": "africa", "292": "europe", "296": "oceania", "300": "europe",
  "304": "north_america", "308": "north_america", "312": "north_america",
  "316": "oceania", "320": "north_america", "324": "africa", "328": "south_america",
  "332": "north_america", "334": "oceania", "336": "europe", "340": "north_america",
  "344": "asia", "348": "europe", "352": "europe", "356": "asia",
  "360": "asia", "364": "asia", "368": "asia", "372": "europe",
  "376": "asia", "380": "europe", "384": "africa", "388": "north_america",
  "392": "asia", "398": "asia", "400": "asia", "404": "africa",
  "408": "asia", "410": "asia", "414": "asia", "417": "asia",
  "418": "asia", "422": "asia", "426": "africa", "428": "europe",
  "430": "africa", "434": "africa", "438": "europe", "440": "europe",
  "442": "europe", "450": "africa", "454": "africa", "458": "asia",
  "462": "asia", "466": "africa", "470": "europe", "478": "africa",
  "480": "africa", "484": "north_america", "492": "europe", "496": "asia",
  "498": "europe", "499": "europe", "500": "north_america", "504": "africa",
  "508": "africa", "512": "asia", "516": "africa", "520": "oceania",
  "524": "asia", "528": "europe", "531": "north_america", "533": "north_america",
  "540": "oceania", "548": "oceania", "554": "oceania", "558": "north_america",
  "562": "africa", "566": "africa", "570": "oceania", "574": "oceania",
  "578": "europe", "580": "oceania", "583": "oceania", "584": "oceania",
  "585": "oceania", "586": "asia", "591": "north_america", "598": "oceania",
  "600": "south_america", "604": "south_america", "608": "asia", "612": "oceania",
  "616": "europe", "620": "europe", "624": "africa", "626": "asia",
  "630": "north_america", "634": "asia", "642": "europe", "643": "europe",
  "646": "africa", "652": "north_america", "654": "africa", "659": "north_america",
  "660": "north_america", "662": "north_america", "663": "north_america",
  "670": "north_america", "674": "europe", "678": "africa", "682": "asia",
  "686": "africa", "688": "europe", "690": "africa", "694": "africa",
  "702": "asia", "703": "europe", "704": "asia", "705": "europe",
  "706": "africa", "710": "africa", "716": "africa", "724": "europe",
  "728": "africa", "729": "africa", "732": "africa", "740": "south_america",
  "744": "europe", "748": "africa", "752": "europe", "756": "europe",
  "760": "asia", "762": "asia", "764": "asia", "768": "africa",
  "772": "oceania", "776": "oceania", "780": "north_america", "784": "asia",
  "788": "africa", "792": "asia", "795": "asia", "798": "oceania",
  "800": "africa", "804": "europe", "807": "europe", "818": "africa",
  "826": "europe", "831": "europe", "832": "europe", "833": "europe",
  "834": "africa", "840": "north_america", "850": "north_america", "854": "africa",
  "858": "south_america", "860": "asia", "862": "south_america", "876": "oceania",
  "882": "oceania", "887": "asia", "894": "africa",
};

const NAME_FALLBACK = {
  "Greenland": "north_america",
  "Antarctica": "oceania",
  "New Caledonia": "oceania",
  "French Southern and Antarctic Lands": "oceania",
  "Western Sahara": "africa",
  "Somaliland": "africa",
  "Kosovo": "europe",
  "Taiwan": "asia",
  "Palestine": "asia",
};

const width = 1000;
const height = 520;

const topo = JSON.parse(fs.readFileSync(topoPath, "utf8"));
const countries = topojson.feature(topo, topo.objects.countries);

const projection = d3.geoNaturalEarth1()
  .fitExtent([[12, 8], [width - 12, height - 8]], countries);

const pathGen = d3.geoPath(projection);

const byContinent = {};
for (const f of countries.features) {
  const id = String(f.id).padStart(3, "0");
  const cont =
    NUMERIC_CONTINENT[id] ||
    NAME_FALLBACK[f.properties?.name] ||
    "asia";
  if (!byContinent[cont]) byContinent[cont] = [];
  byContinent[cont].push(f);
}

const CONTINENT_COLORS = {
  asia: "#c9d6e3",
  europe: "#b8cfe0",
  africa: "#d4c4a8",
  north_america: "#b5d4c8",
  south_america: "#c8ddb8",
  oceania: "#a8d4d4",
};

let svg = `<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${width} ${height}" class="world-map">
  <defs>
    <linearGradient id="oceanGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" style="stop-color:#1a5276"/>
      <stop offset="100%" style="stop-color:#0e3352"/>
    </linearGradient>
    <filter id="landShadow" x="-2%" y="-2%" width="104%" height="104%">
      <feDropShadow dx="0" dy="1" stdDeviation="1.5" flood-opacity="0.25"/>
    </filter>
  </defs>
  <rect width="100%" height="100%" fill="url(#oceanGrad)"/>
  <g filter="url(#landShadow)" id="landmasses">
`;

for (const cont of Object.keys(CONTINENT_COLORS)) {
  const feats = byContinent[cont] || [];
  if (!feats.length) continue;
  const collection = { type: "FeatureCollection", features: feats };
  const d = pathGen(collection);
  if (!d) continue;
  svg += `    <path class="continent-path" data-continent="${cont}" fill="${CONTINENT_COLORS[cont]}" d="${d}"/>\n`;
}

svg += `  </g>
  <g class="graticule" fill="none" stroke="rgba(255,255,255,0.08)" stroke-width="0.5">
`;

const graticule = d3.geoGraticule().step([30, 30]);
svg += `    <path d="${pathGen(graticule())}"/>\n`;
svg += `  </g>
</svg>`;

fs.writeFileSync(outPath, svg);
const kb = (fs.statSync(outPath).size / 1024).toFixed(1);
console.log(`Wrote ${outPath} (${kb} KB)`);
