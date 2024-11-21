<script>
    $('#deleteModal').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget); // Button that triggered the modal
        var articleTitle = button.data('article-title'); // Extract article title
        var articleId = button.data('article-id'); // Extract article ID

        // Update the modal content
        var modal = $(this);
        modal.find('#articleTitle').text(articleTitle);

        // Update the delete confirmation button's URL
        modal.find('#confirmDeleteBtn').attr('href', `/delete/${articleId}/`);
    });
</script>
