<script>
	export const prerender = true;
	import { onMount } from 'svelte';
	let promise;
	onMount(async () => {
		const res = await fetch('http://localhost:1337/app');
		promise = await res.text();
	});
</script>

<main class="container">
	<h1>Welcome to SvelteKit</h1>
	<p>Visit <a href="https://kit.svelte.dev">kit.svelte.dev</a> to read the documentation</p>
	<details>
		<summary>Accordion 2</summary>
		<form>
			<fieldset  class="grid">
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
        <article>I’m a card!</article>
        <article>I’m a card!</article>
        <article>I’m a card!</article>
        <article>I’m a card!</article>
        <article>I’m a card!</article>
        <article>I’m a card!</article>
        <article>I’m a card!</article>
        <article>I’m a card!</article>
        <article>I’m a card!</article>
        <article>I’m a card!</article>
        <article>I’m a card!</article>
        <article>I’m a card!</article>
        <article>I’m a card!</article>
        <article>I’m a card!</article>
        <article>I’m a card!</article>
        <article>I’m a card!</article>
        <article>I’m a card!</article>
        <article>I’m a card!</article>

	{#await promise}
		<p>...waiting</p>
	{:then ret}
		<p>Response from the server was: {ret}</p>
	{:catch error}
		<p style="color: red">{error.message}</p>
	{/await}

	...
</main>
