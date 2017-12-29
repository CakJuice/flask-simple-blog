Comments = window.Comments || {};

(function(exports, $) {
	/* Template string for rendering success or error messages. */
	var alertMarkup = (
		'<div class="alert alert-{class} alert-dismissable">' +
		'<button type="button" class="close" data-dimiss="alert" aria-hidden="true">&times;</button>' +
		'<strong>{title}</strong> {body}</div>'
	);

	/* Create an alert element. */
	function makeAlert(alertClass, title, body) {
		var alertCopy = (alertMarkup.replace('{class}', alertClass)
			.replace('{title}', title).replace('{body}', body));
		return $(alertCopy)
	}

	/* Retrieve the values from the form fields and return as an object. */
	function getFormData(form) {
		return {
			'name': form.find('input#name').val(),
			'email': form.find('input#email').val(),
			'url': form.find('input#url').val(),
			'body': form.find('textarea#body').val(),
			'entry_id': form.find('input[name=entry_id]').val(),
		}
	}

	function bindHandler() {
		/* When the comment form is submitted, serialize the form data as JSON
		and POST it to the API. */ 
		$('form#comment-form').submit(function(event) {
			var form = $(this);
			var formData = getFormData(form);
			var request = $.ajax({
				url: form.attr('action'),
				type: 'POST',
				data: JSON.stringify(formData),
				contentType: 'application/json; charset=utf-8',
				dataType: 'json'
			});
			request.done(function(data) {
				alertDiv = makeAlert('success', 'Success', 'Your comment was posted.');
				form.before(alertDiv);
				form[0].reset();
			});
			request.fail(function(data) {
				alertDiv = makeAlert('danger', 'Error', 'Your comment was not posted.');
				form.before(alertDiv);
			});

			event.preventDefault();
		});
	}

	exports.bindHandler = bindHandler;
}) (Comments, jQuery);