function RankingsList({ rankings }) {

    return (
      <ul>
        {
          rankings.map((ranking) => {
            return <li key = {ranking.restaurant_id}>{ranking.rank_position}. {ranking.name} ({ranking.score})</li>
          })
        }
      </ul>
    )
}

export default RankingsList
