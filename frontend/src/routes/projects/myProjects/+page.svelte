<script>
    import { page } from "$app/stores";

    console.log("$page.data:", $page.data);

    let activeTab = "my";
    let name = '';
    let date = '';
    let time = '';
    let owner = '';
    let description = '';
    let showCreateModal = false;

    export let projects = $page.data.projects;
    //export let sharedProjects;
    console.log("myProjects:", projects);

    function openCreateModal() {
        showCreateModal = true;
    }

    function closeCreateModal() {
        showCreateModal = false;
    }

  async function submitForm(event) {
    event.preventDefault();

    const payload = {
      name,
      date,
      time,
      owner,
      description
    };

    try {
      const res = await fetch('http://localhost:8000/projects/create', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
      });

      if (!res.ok) {
        const error = await res.text();
        console.error('Failed to create project:', error);
        alert('Error creating project');
        return;
      }

      const data = await res.json();
      console.log('Project created:', data);
      alert('Project created successfully!');
      showCreateModal = false;

    } catch (err) {
      console.error('Error:', err);
      alert('Something went wrong.');
    }
  }
</script>

<div class="top-bar">
    <h1>Project Selection</h1>
    <button class="create-btn" on:click={openCreateModal}>+ Create new</button>
</div>

<!-- Recent projects section can stay static or be derived from data later -->
<section class="recent-projects">
    <h2>Recent Projects</h2>
    <div class="recent-list">
        <div class="recent-card">
            Base Perimeter Network<br /><small>Nov 2, 2024</small>
        </div>
        <div class="recent-card">
            Mission Control Portal<br /><small>Nov 1, 2024</small>
        </div>
        <div class="recent-card">
            Field Operations<br /><small>Oct 31, 2024</small>
        </div>
        <div class="recent-card">
            Government Defense<br /><small>Oct 30, 2024</small>
        </div>
    </div>
</section>

<section class="all-projects">
    <h2>All Projects</h2>
    <div class="tabs">
        <button
            on:click={() => (activeTab = "my")}
            class:active={activeTab === "my"}>My Projects</button
        >
        <button
            on:click={() => (activeTab = "shared")}
            class:active={activeTab === "shared"}>Shared Projects</button
        >
    </div>

    <table>
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
                    <td>{new Date(project.editTime).toLocaleString()}</td>
                    <td>{project.owner}</td>
                </tr>
            {/each}
        </tbody>
    </table>
</section>

{#if showCreateModal}
        <div
        class="modal-overlay"
        on:click={closeCreateModal}
        on:keydown={(e) => e.key === 'Enter' && closeCreateModal()}
        tabindex="0"
        role="button"
        aria-label="Close modal"
        >
        <!-- TODO: FIX THESE WARNINGS-->
        <!-- svelte-ignore a11y_click_events_have_key_events -->
        <!-- svelte-ignore a11y_no_static_element_interactions -->
        <div class="modal" on:click|stopPropagation>
            <div class="modal-header">
                <h2>Create Project</h2>
                <button class="close-btn" on:click={closeCreateModal}>×</button>
            </div>

            <form on:submit={submitForm}>
                <div class="form-grid">
                    <label>
                        Project Name *
                        <input required bind:value={name} />
                      </label>
                      
                      <label>
                        Start Date *
                        <input type="date" required bind:value={date} />
                      </label>
                      
                      <label>
                        Time *
                        <input type="time" required bind:value={time} />
                      </label>
                      
                      <label>
                        Lead Analyst Initials *
                        <input required bind:value={owner} />
                      </label>
                      
                      <label class="description-field" style="grid-column: span 2;">
                        Project Description
                        <textarea rows="3" bind:value={description}></textarea>
                      </label>

                    <label style="grid-column: span 2;">
                        Upload NMap
                        <input type="file" multiple />
                    </label>
                </div>

                <div class="modal-actions">
                    <button
                        type="button"
                        class="cancel-btn"
                        on:click={closeCreateModal}>Cancel</button
                    >
                    <button type="submit" class="submit-btn">Create</button>
                </div>
            </form>
        </div>
    </div>
{/if}

<style>
    .modal-overlay {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-color: rgba(0, 0, 0, 0.5);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 50;
    }

    .modal {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        width: 600px;
        max-width: 95%;
        position: relative;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
    }

    .modal-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
    }

    .modal-header h2 {
        margin: 0;
    }

    .close-btn {
        background: none;
        border: none;
        font-size: 1.5rem;
        line-height: 1;
        cursor: pointer;
    }

    .form-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1rem;
    }

    .form-grid label {
        display: flex;
        flex-direction: column;
        font-weight: 500;
        font-size: 0.9rem;
    }

    input,
    textarea {
        margin-top: 0.25rem;
        padding: 0.5rem;
        border-radius: 6px;
        border: 1px solid #ccc;
        font-size: 0.9rem;
    }

    textarea {
        resize: vertical;
    }

    .modal-actions {
        display: flex;
        justify-content: flex-end;
        gap: 1rem;
        margin-top: 1.5rem;
    }

    .cancel-btn {
        background: #1f2937;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 6px;
        cursor: pointer;
    }

    .submit-btn {
        background: #14b8a6;
        color: white;
        border: none;
        padding: 0.5rem 1.25rem;
        border-radius: 6px;
        font-weight: bold;
        cursor: pointer;
    }

    .submit-btn:hover {
        background: #0d9488;
    }

    h1 {
        font-size: 1.8rem;
        margin-bottom: 1rem;
    }

    .recent-list {
        display: flex;
        gap: 1rem;
        margin-bottom: 2rem;
    }

    .recent-card {
        border: 1px solid #ccc;
        padding: 1rem;
        border-radius: 8px;
        background: white;
        min-width: 160px;
        text-align: center;
    }

    .tabs {
        display: flex;
        gap: 1rem;
        margin-bottom: 1rem;
    }

    .tabs button {
        border: none;
        background: none;
        font-weight: bold;
        padding-bottom: 0.25rem;
        cursor: pointer;
        border-bottom: 2px solid transparent;
    }

    .tabs button.active {
        border-color: teal;
        color: teal;
    }

    table {
        width: 100%;
        border-spacing: 0;
        border-collapse: collapse;
        background: white;
        border-radius: 8px;
        overflow: hidden;
    }

    th,
    td {
        padding: 1rem;
        text-align: left;
        border-bottom: 1px solid #e5e7eb;
    }

    .top-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
    }

    .create-btn {
        background-color: #38bdf8; /* teal-ish blue */
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-weight: bold;
        cursor: pointer;
        transition: background-color 0.2s ease-in-out;
    }

    .create-btn:hover {
        background-color: #0ea5e9;
    }
</style>
