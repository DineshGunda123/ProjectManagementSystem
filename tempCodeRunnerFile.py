class Review(models.Model):
    project = models.ForeignKey(create_project, related_name='reviews', on_delete=models.CASCADE)
    order = models.PositiveIntegerField()
    completed = models.BooleanField(default=False)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    feedback = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('project', 'order')

    def __str__(self):
        return f"Review {self.order} for {self.project.projectname}"    