<script lang="ts">
	export const prerender = true;
	import '../app.css';
	import { onMount } from 'svelte';
	let promise;
	//onMount(async () => {
	//	const res = await fetch('http://localhost:1337/app');
	//	promise = await res.text();
	//});
	import Leaflet from '$lib/Leaflet.svelte';
	import Marker from '$lib/Marker.svelte';
	import Popup from '$lib/Popup.svelte';
	const initialView: LatLngExpression = [40.776676, -73.971321]; // Manhattan

	import testpages from '../test_violation_pages.json';
	import { writable } from 'svelte/store';
	const current_page = writable(testpages.page1);
</script>

<main class="container">
	<h1>Welcome to SvelteKit</h1>
	<p>Visit <a href="https://kit.svelte.dev">kit.svelte.dev</a> to read the documentation</p>
	<details>
		<summary>Accordion 2</summary>
		<form>
			<fieldset class="grid">
				<label>
					First name
					<input name="first_name" placeholder="First name" autocomplete="given-name" />
				</label>
				<label>
					Email
					<input type="email" name="email" placeholder="Email" autocomplete="email" />
				</label>
			</fieldset>

			<input type="submit" value="Subscribe" />
		</form>
	</details>
	<div class="grid" id="mapresult">
		<Leaflet view={initialView} zoom={13}>
			{#each $current_page as result}
				<Marker latLng={[result.Latitude, result.Longitude]} width={10} height={10}>
					<Popup>{result.DBA}</Popup>
				</Marker>
			{/each}
		</Leaflet>
		<div class="results overflow-auto">
			{#each $current_page as result}
				<article>{result.DBA}</article>
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
