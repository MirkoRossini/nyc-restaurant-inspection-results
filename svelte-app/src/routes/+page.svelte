<script lang="ts">
	export const prerender = true;
	import '../app.css';
	import { onMount } from 'svelte';
	import testpages from '../test_violation_pages.json';
	import testViolationHistories from '../test_violation_histories.json';
	import descriptions from '../descriptions.json';
	let isFiltersOpen = false;

	function toggleFiltersCallback(open: boolean) {
		isFiltersOpen = open;
		console.log("toggle", isFiltersOpen, open);
	}
	
	function formatTimestampToAmericanDate(timestamp: number): string {
		const date = new Date(timestamp * 1000); // Convert to milliseconds
		const month = date.getMonth() + 1; // Months are 0-based
		const day = date.getDate();
		const year = date.getFullYear();

		return `${month}/${day}/${year}`;
	}
	function handleSubmit(event) {
		event.preventDefault(); // Prevent page refresh
		const formData = new FormData(event.target);
		let values = new Map<string, string[]>();
		formData.forEach((value, key) => {
			if (!values.get(key)) {
				values.set(key, []);
			}
			values.get(key)!.push(value);
		});
		console.log(formData, values);
		toggleFiltersCallback(false);
  	}
	let promise;
	//onMount(async () => {
	//	const res = await fetch('http://localhost:1337/app');
	//	promise = await res.text();
	//});

	const FIELDS = [
		'CAMIS',
		'INSPECTION DATE',
		'DBA',
		'GRADE',
		'Latitude',
		'Longitude',
		'VIOLATION CODE',
		'SCORE',
		'VIOLATION DESCRIPTION KEY'
	];

	const LATITUDE_IDX = FIELDS.indexOf('Latitude');
	const LONGITUDE_IDX = FIELDS.indexOf('Longitude');
	const GRADE_IDX = FIELDS.indexOf('GRADE');
	const DBA_IDX = FIELDS.indexOf('DBA');
	const CAMIS_IDX = FIELDS.indexOf('CAMIS');
	const INSPECTION_DATE_IDX = FIELDS.indexOf('INSPECTION DATE');
	const VIOLATION_DESCRIPTION_KEY_IDX = FIELDS.indexOf('VIOLATION DESCRIPTION KEY');

	async function getHistory(inspection: Array<number | string>) {
		// Hit the server here.
		return testViolationHistories[inspection[CAMIS_IDX]];
	}

	import Leaflet from '$lib/Leaflet.svelte';
	import Marker from '$lib/Marker.svelte';
	import Popup from '$lib/Popup.svelte';
	let initialView: LatLngExpression = [40.776676, -73.971321]; // Manhattan

	import { writable } from 'svelte/store';
	const current_page = writable(testpages.page0);
</script>

<main class="container">
	<h1>NYC Inspection results</h1>
	<details bind:open={isFiltersOpen}
	 on:toggle={e =>  toggleFiltersCallback(e.target.open) }>
		<summary>Filters</summary>
		<form on:submit={handleSubmit}>
			<fieldset class="grid">
				<label>
					Name
					<input name="restaurant_name" placeholder="Restaurant name" />
				</label>
			</fieldset>
			<fieldset class="grid">
				<legend>NYC Restaurant Grades</legend>

				<label>
					<input type="checkbox" name="grade" value="A" checked>
					A
				</label>

				<label>
					<input type="checkbox" name="grade" value="B" checked>
					B
				</label>

				<label>
					<input type="checkbox" name="grade" value="C" checked>
					C
				</label>

				<label>
					<input type="checkbox" name="grade" value="N">
					Not Graded
				</label>
			</fieldset>

			<input type="submit" value="Update filters" />
		</form>
	</details>
	<div class="grid" id="mapresult">
		<Leaflet view={initialView} zoom={13}>
			{#each $current_page as result}
				<Marker
					latLng={[result[LATITUDE_IDX], result[LONGITUDE_IDX]]}
					grade={result[GRADE_IDX]}
					width={10}
					height={10}
				>
					<Popup>
						<div class="history-popup">
							<h1 class="popup-restaurant-name">{result[DBA_IDX]}</h1>
							<div class="overflow-auto history">
								{#await getHistory(result)}
									<p>...waiting</p>
								{:then history}
									{#each history as past_hist}
										<p>
											Grade {past_hist[GRADE_IDX - 1]}, On {formatTimestampToAmericanDate(
												past_hist[INSPECTION_DATE_IDX - 1]
											)}:
											{descriptions[past_hist[VIOLATION_DESCRIPTION_KEY_IDX - 1]]}
										</p>
									{/each}
								{:catch error}
									<p style="color: red">{error.message}</p>
								{/await}
							</div>
						</div>
					</Popup>
				</Marker>
			{/each}
		</Leaflet>
		<div class="results overflow-auto">
			{#each $current_page as result}
				<article>
					<details>
						<summary>{result[DBA_IDX]}</summary>

						{#await getHistory(result)}
							<p>...waiting</p>
						{:then history}
							{#each history as past_hist}
								<p>
									Grade {past_hist[GRADE_IDX - 1]}, On {formatTimestampToAmericanDate(
										past_hist[INSPECTION_DATE_IDX - 1]
									)}:
									{descriptions[past_hist[VIOLATION_DESCRIPTION_KEY_IDX - 1]]}
								</p>
							{/each}
						{:catch error}
							<p style="color: red">{error.message}</p>
						{/await}
					</details>
				</article>
			{/each}
		</div>
	</div>
	<!-- 
	{#await promise}
		<p>...waiting</p>
	{:then ret}
		<p>Response from the server was: {ret}</p>
	{:catch error}
		<p style="color: red">{error.message}</p>
	{/await} -->

	...
</main>
