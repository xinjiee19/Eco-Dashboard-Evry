from django.db import models

class MessageSensibilisation(models.Model):
    TYPE_CHOICES = [
        ('INFO', 'Information'),
        ('CONSEIL', 'Conseil'),
        ('ALERTE', 'Alerte'),
        ('OBJECTIF', 'Objectif'),
    ]
    
    TYPE_CONTENU_CHOICES = [
        ('message', 'Message / Conseil'),
        ('zoom', 'Zoom sur une Action'),
    ]

    titre = models.CharField(max_length=200, default="Le mot de la Mairie")
    contenu = models.TextField(help_text="Le message à afficher sur le tableau de bord.")
    type_message = models.CharField(max_length=20, choices=TYPE_CHOICES, default='INFO')
    type_contenu = models.CharField(
        max_length=20, 
        choices=TYPE_CONTENU_CHOICES, 
        default='message',
        verbose_name="Type de contenu",
        help_text="Message = conseil général, Zoom = action spécifique à mettre en avant"
    )
    actif = models.BooleanField(default=True, help_text="Cochez pour afficher ce message sur le dashboard.")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Message de Sensibilisation"
        verbose_name_plural = "Messages de Sensibilisation"
        ordering = ['-created_at']

    def __str__(self):
        return self.titre
