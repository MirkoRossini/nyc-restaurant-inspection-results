<script>
export const prerender = true;
import {onMount} from 'svelte';
let promise;
onMount(async () => {
		const res = await fetch('http://localhost:1337/app');
                promise = await res.text();
});


</script>
<h1>Welcome to SvelteKit</h1>
<p>Visit <a href="https://kit.svelte.dev">kit.svelte.dev</a> to read the documentation</p>

{#await promise}
<p>...waiting </p>
{:then ret}
                <p>Response from the server was: {ret} </p>
{:catch error}
	<p style="color: red">{error.message}</p>
{/await}
