class UserFeedback:
    def __init__(self):
        self.likes = 0
        self.dislikes = 0

    def record_feedback(self, feedback):
        """Records user feedback as either a like (1) or dislike (0)."""
        if feedback == 1:
            self.likes += 1
        elif feedback == 0:
            self.dislikes += 1
        else:
            raise ValueError("Feedback should be either 1 (like) or 0 (dislike).")

    def get_feedback_summary(self):
        """Returns the total number of likes and dislikes."""
        return {
            'total_likes': self.likes,
            'total_dislikes': self.dislikes
        }

    def reset_feedback(self):
        """Resets the feedback counts."""
        self.likes = 0
        self.dislikes = 0
