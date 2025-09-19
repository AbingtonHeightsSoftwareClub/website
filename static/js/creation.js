if (window.history.replaceState) {
  window.history.replaceState(null, null, window.location.href);
}

function deletePerson(id) {
  fetch("/delete_player/" + id, {
    method: "DELETE",
  })
    .then((response) => {
      if (response.ok) {
        window.location.reload();
      } else {
        console.error("Failed to delete item with id: ", id);
      }
    })
    .catch((error) => {
      console.error("Error during fetching:", error);
    });
}
