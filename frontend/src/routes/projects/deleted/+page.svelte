<script lang="ts">
	import {
        submitBanishForm,
        submitRestoreForm,
        openMenuFor,
        toggleMenu,
	} from './deletedLogic';

	export let data;
	let projects = data.projects;

	console.log('myProjects:', projects);
</script>

<div class="page-wrapper">
	<div class="top-bar">
		<h1>Deleted Projects</h1>
	</div>

	<section class="all-projects">
		<div class="table-wrapper">
			<table class="w-full h-full table-auto border">
				<thead>
					<tr>
						<th>Project Name</th>
						<th>Last Edit</th>
						<th>Lead Analyst</th>
						<th></th>
					</tr>
				</thead>
				<tbody>
					{#each projects as project}
						<tr>
							<td>{project.name}</td>
							<td>{new Date(project.editTime).toLocaleDateString()}</td>
							<td>{project.owner}</td>
							<td>Run Scan</td>
							<td class="actions-cell">
								<div class="menu-wrapper">
									<button class="dots-btn" on:click={(e) => toggleMenu(project.name, e)}>⋯</button>

									{#if $openMenuFor === project.name}
										<!-- svelte-ignore a11y_click_events_have_key_events -->
										<!-- svelte-ignore a11y_no_static_element_interactions -->
										<div class="dropdown-menu" on:click|stopPropagation>
											<button on:click={() => {submitRestoreForm(project.name);}}>Restore</button>
											<button on:click={() => {submitBanishForm(project.name);}}>Delete Forever</button>
										</div>
									{/if}
								</div>
							</td>
						</tr>
					{/each}
				</tbody>
			</table>
		</div>
	</section>
</div>