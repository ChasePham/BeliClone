function UserSwitcher({ users, currentUserId, onChange }) {

    return (
      <select
        value = {currentUserId}
        onChange = {(event) => onChange(Number(event.target.value))}
      >
        {
          users.map((user) => {
            return <option key = {user.id} value = {user.id}>{user['display_name']}</option>
          })
        }
      </select>
    )
}

export default UserSwitcher
