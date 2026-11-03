import jenkins.model.Jenkins
import hudson.security.HudsonPrivateSecurityRealm
import hudson.security.FullControlOnceLoggedInAuthorizationStrategy
import jenkins.install.InstallState

def jenkins = Jenkins.get()
if (!(jenkins.securityRealm instanceof HudsonPrivateSecurityRealm)) {
    def realm = new HudsonPrivateSecurityRealm(false)
    realm.createAccount('emaad', new File('/run/secrets/jenkins-admin-password').text.trim())
    jenkins.setSecurityRealm(realm)
    def authorization = new FullControlOnceLoggedInAuthorizationStrategy()
    // Localhost-only lab: permit viewing results; all writes require the local account.
    authorization.setAllowAnonymousRead(true)
    jenkins.setAuthorizationStrategy(authorization)
}
jenkins.setNumExecutors(1)
jenkins.setInstallState(InstallState.INITIAL_SETUP_COMPLETED)
jenkins.save()
