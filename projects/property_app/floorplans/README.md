# Floor plans

## How to use

1. Save floor plan images (JPG/PNG/PDF) into `inbox/`. Any filename works.
2. Optionally add a row per file to `listing_details.csv` (the `file` column must match the exact filename). Leave blank anything you don't have yet.
   - `role`: `comp` or `subject`
   - `type`: `house` or `townhouse`
   - `dates`: `YYYY-MM-DD`
   - `prices`: whole dollars
   - For a price guide with a single figure, populate `guide_low` only. For a sold result, populate `sold_price` and `sold_date`.
3. Tell Claude **"process floor plans"**. Claude will read address/beds/baths/cars, estimate internal m², merge CSV details, add rows to the Property Valuer dashboard, then move each file to `processed/`.
