// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

// import "@openzeppelin/contracts/access/AccessControl.sol";
// import "@openzeppelin/contracts/utils/Counters.sol";

contract EvidenceLedger is AccessControl {
    using Counters for Counters.Counter;
    Counters.Counter private _evidenceIds;
    Counters.Counter private _tipIds;

    bytes32 public constant POLICE_ROLE = keccak256("POLICE_ROLE");

    // ------------------ Structs ------------------
    struct Case {
        uint256 caseId;
        string metadataHash;
        address creator;
        bytes casePublicKey;
        uint256 createdAt;
        bool isOpen;
    }

    struct Evidence {
        uint256 evidenceId;
        uint256 caseId;
        string sha256Hash;
        string cidPreview;
        address submitter;
        uint8 submitterType;
        bool approved;
        uint256 submittedAt;
        string encryptedKeyRef;
    }

    struct Tip {
        uint256 tipId;
        string message;
        address submitter;
        uint256 submittedAt;
        bool linkedToCase;
        uint256 caseId;
    }

    struct Report {
        uint256 reportId;
        uint256 caseId;
        string reportCid;
        address reporter;
        uint256 generatedAt;
    }

    // ------------------ Mappings ------------------
    mapping(uint256 => Case) public cases;
    mapping(uint256 => Evidence) public evidences;
    mapping(uint256 => Tip) public tips;
    mapping(uint256 => Report) public reports;
    mapping(uint256 => uint256[]) public caseEvidences;
    mapping(uint256 => uint256[]) public caseTips;

    // ------------------ Events ------------------
    event PoliceVerified(address indexed officer);
    event CaseCreated(uint256 indexed caseId, address indexed creator, string metadataHash, uint256 timestamp);
    event EvidenceSubmitted(uint256 indexed caseId, uint256 indexed evidenceId, string sha256Hash, address submitter, uint8 submitterType, string cidPreview, uint256 timestamp);
    event EvidenceApproved(uint256 indexed caseId, uint256 indexed evidenceId, address approver, uint256 timestamp);
    event TipSubmitted(uint256 indexed tipId, string message, address submitter, uint256 timestamp);
    event TipLinkedToCase(uint256 indexed tipId, uint256 indexed caseId, uint256 timestamp);
    event ReportAdded(uint256 indexed reportId, uint256 indexed caseId, string reportCid, uint256 timestamp);

    // ------------------ Constructor ------------------
    constructor() {
        _grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
    }

    // ------------------ Role Management ------------------
    function addPoliceOfficer(address officer) external onlyRole(DEFAULT_ADMIN_ROLE) {
        _grantRole(POLICE_ROLE, officer);
    }

    function addPoliceOfficerWithVerification(address officer, bytes calldata proof) external onlyRole(DEFAULT_ADMIN_ROLE) {
        require(_verifyOfficer(officer, proof), "Officer identity not verified");
        _grantRole(POLICE_ROLE, officer);
        emit PoliceVerified(officer);
    }

    function _verifyOfficer(address officer, bytes memory proof) internal pure returns (bool) {
        officer; proof; // silence warnings
        return true; // Always true for MVP
    }

    function isPolice(address account) external view returns (bool) {
        return hasRole(POLICE_ROLE, account);
    }

    function isAdmin(address account) external view returns (bool) {
        return hasRole(DEFAULT_ADMIN_ROLE, account);
    }

    // ------------------ Case Functions ------------------
    function createCaseWithId(
        uint256 caseId, 
        string calldata metadataHash, 
        bytes calldata casePublicKey
    ) 
        external 
        onlyRole(POLICE_ROLE) 
    {
        require(cases[caseId].caseId == 0, "Case exists");
        cases[caseId] = Case({
            caseId: caseId,
            metadataHash: metadataHash,
            creator: msg.sender,
            casePublicKey: casePublicKey,
            createdAt: block.timestamp,
            isOpen: true
        });
        emit CaseCreated(caseId, msg.sender, metadataHash, block.timestamp);
    }

    // ------------------ Evidence Functions ------------------
    function submitEvidenceToCase(
        uint256 caseId, 
        string calldata sha256Hash, 
        string calldata cidPreview, 
        uint8 submitterType, 
        string calldata encryptedKeyRef
    ) 
        external 
        returns (uint256) 
    {
        require(cases[caseId].caseId != 0, "Case not found");
        _evidenceIds.increment();
        uint256 eid = _evidenceIds.current();
        evidences[eid] = Evidence({
            evidenceId: eid,
            caseId: caseId,
            sha256Hash: sha256Hash,
            cidPreview: cidPreview,
            submitter: (submitterType == 0 ? address(0) : msg.sender),
            submitterType: submitterType,
            approved: false,
            submittedAt: block.timestamp,
            encryptedKeyRef: encryptedKeyRef
        });
        caseEvidences[caseId].push(eid);
        emit EvidenceSubmitted(caseId, eid, sha256Hash, (submitterType == 0 ? address(0) : msg.sender), submitterType, cidPreview, block.timestamp);
        return eid;
    }

    function approveEvidence(uint256 caseId, uint256 evidenceId) external onlyRole(POLICE_ROLE) {
        Evidence storage e = evidences[evidenceId];
        require(e.caseId == caseId, "Mismatch");
        e.approved = true;
        emit EvidenceApproved(caseId, evidenceId, msg.sender, block.timestamp);
    }

    // ------------------ Tip Functions ------------------
    function submitTip(string calldata message) external returns (uint256) {
        _tipIds.increment();
        uint256 tipId = _tipIds.current();
        tips[tipId] = Tip({
            tipId: tipId,
            message: message,
            submitter: msg.sender,
            submittedAt: block.timestamp,
            linkedToCase: false,
            caseId: 0
        });
        emit TipSubmitted(tipId, message, msg.sender, block.timestamp);
        return tipId;
    }

    function linkTipToCase(uint256 tipId, uint256 caseId) external onlyRole(POLICE_ROLE) {
        require(cases[caseId].caseId != 0, "Case not found");
        Tip storage t = tips[tipId];
        require(!t.linkedToCase, "Tip already linked");
        t.linkedToCase = true;
        t.caseId = caseId;
        caseTips[caseId].push(tipId);
        emit TipLinkedToCase(tipId, caseId, block.timestamp);
    }

    // ------------------ Report Functions ------------------
    function addReport(uint256 caseId, string calldata reportCid) external returns (uint256) {
        require(cases[caseId].caseId != 0, "Case not found");
        uint256 reportId = uint256(keccak256(abi.encodePacked(reportCid, block.timestamp)));
        reports[reportId] = Report({
            reportId: reportId,
            caseId: caseId,
            reportCid: reportCid,
            reporter: msg.sender,
            generatedAt: block.timestamp
        });
        emit ReportAdded(reportId, caseId, reportCid, block.timestamp);
        return reportId;
    }
}
