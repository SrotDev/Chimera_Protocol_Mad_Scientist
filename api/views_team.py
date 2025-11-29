"""
Team Management Views
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Workspace, TeamMember, WorkspaceInvitation, User
from .serializers_v2 import (
    TeamMemberSerializer, TeamInviteSerializer,
    TeamRoleUpdateSerializer, TeamStatusUpdateSerializer
)
from django.utils import timezone


def api_response(ok=True, data=None, error=None):
    """Standard API response envelope"""
    return {'ok': ok, 'data': data, 'error': error}


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_team_members_view(request, workspace_id):
    """List all team members in a workspace"""
    try:
        workspace = Workspace.objects.get(id=workspace_id)
        
        # Check if user has access
        is_owner = workspace.owner == request.user
        is_member = workspace.members.filter(user=request.user).exists()
        
        if not (is_owner or is_member):
            return Response(
                api_response(ok=False, error='Access denied'),
                status=status.HTTP_403_FORBIDDEN
            )
        
        members = workspace.members.all()
        serializer = TeamMemberSerializer(members, many=True)
        
        return Response(api_response(
            ok=True,
            data={
                'members': serializer.data,
                'total': members.count()
            }
        ))
    
    except Workspace.DoesNotExist:
        return Response(
            api_response(ok=False, error='Workspace not found'),
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def invite_team_member_view(request, workspace_id):
    """Send invitation to a user to join workspace"""
    try:
        workspace = Workspace.objects.get(id=workspace_id)
        
        # Only owner or members can invite
        is_owner = workspace.owner == request.user
        is_member = workspace.members.filter(user=request.user).exists()
        
        if not (is_owner or is_member):
            return Response(
                api_response(ok=False, error='Access denied'),
                status=status.HTTP_403_FORBIDDEN
            )
        
        email = request.data.get('email')
        if not email:
            return Response(
                api_response(ok=False, error='Email is required'),
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Find user by email
        try:
            invitee = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                api_response(ok=False, error='User not found with this email'),
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Can't invite yourself
        if invitee == request.user:
            return Response(
                api_response(ok=False, error='Cannot invite yourself'),
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if already a member
        if workspace.members.filter(user=invitee).exists() or workspace.owner == invitee:
            return Response(
                api_response(ok=False, error='User is already a member of this workspace'),
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if invitation already exists
        existing = WorkspaceInvitation.objects.filter(
            workspace=workspace,
            invitee=invitee,
            status='pending'
        ).first()
        
        if existing:
            return Response(
                api_response(ok=False, error='Invitation already sent to this user'),
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create invitation
        invitation = WorkspaceInvitation.objects.create(
            workspace=workspace,
            inviter=request.user,
            invitee=invitee,
            status='pending'
        )
        
        return Response(
            api_response(ok=True, data={
                'id': invitation.id,
                'workspaceId': workspace.id,
                'workspaceName': workspace.name,
                'inviteeEmail': invitee.email,
                'status': invitation.status,
                'createdAt': invitation.created_at.isoformat(),
                'message': 'Invitation sent successfully'
            }),
            status=status.HTTP_201_CREATED
        )
    
    except Workspace.DoesNotExist:
        return Response(
            api_response(ok=False, error='Workspace not found'),
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_member_role_view(request, workspace_id, user_id):
    """Update team member role"""
    try:
        workspace = Workspace.objects.get(id=workspace_id)
        
        # Only owner or admin can update roles
        is_owner = workspace.owner == request.user
        is_admin = workspace.members.filter(
            user=request.user, 
            role='admin'
        ).exists()
        
        if not (is_owner or is_admin):
            return Response(
                api_response(ok=False, error='Only admins can update roles'),
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = TeamRoleUpdateSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                api_response(ok=False, error=serializer.errors),
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get team member
        try:
            target_user = User.objects.get(id=user_id)
            team_member = workspace.members.get(user=target_user)
        except (User.DoesNotExist, TeamMember.DoesNotExist):
            return Response(
                api_response(ok=False, error='Team member not found'),
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Cannot change owner's role
        if target_user == workspace.owner:
            return Response(
                api_response(ok=False, error='Cannot change owner role'),
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Update role
        team_member.role = serializer.validated_data['role']
        team_member.save()
        
        response_serializer = TeamMemberSerializer(team_member)
        
        return Response(api_response(ok=True, data=response_serializer.data))
    
    except Workspace.DoesNotExist:
        return Response(
            api_response(ok=False, error='Workspace not found'),
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_team_member_view(request, workspace_id, user_id):
    """Remove team member from workspace"""
    try:
        workspace = Workspace.objects.get(id=workspace_id)
        
        # Only owner or admin can remove members
        is_owner = workspace.owner == request.user
        is_admin = workspace.members.filter(
            user=request.user, 
            role='admin'
        ).exists()
        
        if not (is_owner or is_admin):
            return Response(
                api_response(ok=False, error='Only admins can remove members'),
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Get team member
        try:
            target_user = User.objects.get(id=user_id)
            team_member = workspace.members.get(user=target_user)
        except (User.DoesNotExist, TeamMember.DoesNotExist):
            return Response(
                api_response(ok=False, error='Team member not found'),
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Cannot remove owner
        if target_user == workspace.owner:
            return Response(
                api_response(ok=False, error='Cannot remove workspace owner'),
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Remove member
        team_member.delete()
        
        return Response(api_response(
            ok=True,
            data={'message': 'Team member removed successfully'}
        ))
    
    except Workspace.DoesNotExist:
        return Response(
            api_response(ok=False, error='Workspace not found'),
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_member_status_view(request, workspace_id, user_id):
    """Update team member status (online/away/offline)"""
    try:
        workspace = Workspace.objects.get(id=workspace_id)
        
        # Check if user has access
        is_owner = workspace.owner == request.user
        is_member = workspace.members.filter(user=request.user).exists()
        
        if not (is_owner or is_member):
            return Response(
                api_response(ok=False, error='Access denied'),
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = TeamStatusUpdateSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                api_response(ok=False, error=serializer.errors),
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get team member
        try:
            target_user = User.objects.get(id=user_id)
            team_member = workspace.members.get(user=target_user)
        except (User.DoesNotExist, TeamMember.DoesNotExist):
            return Response(
                api_response(ok=False, error='Team member not found'),
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Users can only update their own status
        if target_user != request.user:
            return Response(
                api_response(ok=False, error='Can only update your own status'),
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Update status
        team_member.status = serializer.validated_data['status']
        team_member.save()
        
        response_serializer = TeamMemberSerializer(team_member)
        
        return Response(api_response(ok=True, data=response_serializer.data))
    
    except Workspace.DoesNotExist:
        return Response(
            api_response(ok=False, error='Workspace not found'),
            status=status.HTTP_404_NOT_FOUND
        )


# ============================================
# INVITATION ENDPOINTS
# ============================================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_invitations_view(request):
    """List all pending invitations for the current user"""
    invitations = WorkspaceInvitation.objects.filter(
        invitee=request.user,
        status='pending'
    ).select_related('workspace', 'inviter')
    
    data = []
    for inv in invitations:
        data.append({
            'id': inv.id,
            'workspaceId': inv.workspace.id,
            'workspaceName': inv.workspace.name,
            'inviterName': inv.inviter.name if hasattr(inv.inviter, 'name') else inv.inviter.username,
            'inviterEmail': inv.inviter.email,
            'status': inv.status,
            'createdAt': inv.created_at.isoformat(),
        })
    
    return Response(api_response(ok=True, data={
        'invitations': data,
        'total': len(data)
    }))


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def accept_invitation_view(request, invitation_id):
    """Accept a workspace invitation"""
    try:
        invitation = WorkspaceInvitation.objects.get(
            id=invitation_id,
            invitee=request.user,
            status='pending'
        )
        
        # Update invitation status
        invitation.status = 'accepted'
        invitation.responded_at = timezone.now()
        invitation.save()
        
        # Add user as team member with admin role (full access)
        TeamMember.objects.create(
            user=request.user,
            workspace=invitation.workspace,
            role='admin',
            status='online'
        )
        
        return Response(api_response(ok=True, data={
            'message': 'Invitation accepted',
            'workspaceId': invitation.workspace.id,
            'workspaceName': invitation.workspace.name
        }))
    
    except WorkspaceInvitation.DoesNotExist:
        return Response(
            api_response(ok=False, error='Invitation not found'),
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def decline_invitation_view(request, invitation_id):
    """Decline a workspace invitation"""
    try:
        invitation = WorkspaceInvitation.objects.get(
            id=invitation_id,
            invitee=request.user,
            status='pending'
        )
        
        # Update invitation status
        invitation.status = 'declined'
        invitation.responded_at = timezone.now()
        invitation.save()
        
        return Response(api_response(ok=True, data={
            'message': 'Invitation declined'
        }))
    
    except WorkspaceInvitation.DoesNotExist:
        return Response(
            api_response(ok=False, error='Invitation not found'),
            status=status.HTTP_404_NOT_FOUND
        )
