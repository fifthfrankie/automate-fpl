<script>
    export let players = [];
</script>

<style>
    table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 20px;
    }
    th, td {
        border: 1px solid #ddd;
        padding: 8px;
        text-align: left;
    }
    th {
        background-color: #f4f4f4;
    }
</style>

<h2>Optimized Team</h2>

<table>
    <thead>
        <tr>
            <th>Name</th>
            <th>Team</th>
            <th>Position</th>
            <th>Cost (£M)</th>
            <th>Total Points</th>
        </tr>
    </thead>
    <tbody>
        {#each players as player}
            <tr>
                <td>{player.name}</td>
                <td>{player.team}</td>
                <td>{player.position}</td>
                <td>{player.cost.toFixed(1)}</td>
                <td>{player.total_points}</td>
            </tr>
        {/each}
    </tbody>
</table>