#tsc proxy.ts
#tsc utils.ts
#tsc fetch_flight.ts
#tsc script.ts
#browserify script.js proxy.js utils.js fetch_flight.js > bundle.js
#browserify script.ts proxy.ts utils.ts fetch_flight.ts > bundle.js
browserify script.ts proxy.ts utils.ts fetch_flight.ts -p [ tsify --noImplicitAny ] > bundle.js

