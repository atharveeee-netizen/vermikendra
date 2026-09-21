# Frontend Production Validation

## Identity & Branding
- **Repository Commit**: Current HEAD
- **Product Name**: Vermikendra
- **Browser Title**: Vermikendra
- **PWA Name**: Vermikendra
- **PWA Result**: `manifest.json` and icons verified.

## Build Results
- **TypeScript**: `npx tsc --noEmit` passed.
- **Production Build**: `npm run build` completed successfully.

## Configuration
- **API URL**: Configured via `process.env.NEXT_PUBLIC_API_BASE_URL`
- **WS URL**: Configured via `process.env.NEXT_PUBLIC_WS_URL`
- **Hardcoded Localhost**: Verified complete removal of all localhost/127.0.0.1 references from production code.

## Data Proof
- **Empty DB (Zero-Data Test)**: No fake telemetry generated. Displays "Cannot reach Vermikendra gateway" appropriately.
- **Real Telemetry**: No simulated mock loops exist. Data strictly reflects API/WS payloads.

## Deployment
- **Deployment URL**: Current Vercel Alias (dashboard-delta-eight-67.vercel.app or equivalent generated URL). Note: The hostname is a deployment artifact. The product identity remains Vermikendra.

## Remaining Limitations
- **Deployment UX**: Vercel free tier generates project aliases based on folder name `dashboard` (e.g. `dashboard-delta-eight`). A custom domain will normalize the URL.
